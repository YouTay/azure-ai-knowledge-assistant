# GitHub Actions → Azure Container Apps (ACA) Playbook

Ziel: Der Bot soll CI/CD Workflows korrekt schreiben (Build-only, Build+Push, Build+Push+Deploy) inkl. Secrets & RBAC.

---

## Golden Rules (MUST)

1) **Login in GitHub Actions immer über ein JSON Secret**
- Name: `AZURE_CREDENTIALS`
- Format: JSON von Azure CLI (`--json-auth`)
- In YAML: `azure/login@v2` mit `creds: ${{ secrets.AZURE_CREDENTIALS }}`

2) **Nie einzelne Felder (client-id, client-secret, tenant-id) als Login-Inputs mixen**
- Das führt leicht zu OIDC/secret Verwechslungen und instabilen Pipelines.

3) **Nie Service Principal JSON als Datei committen**
- Kein `sp.json` im Repo.
- GitHub Push Protection blockiert.
- Wenn passiert: Secret rotieren + History scrubben.

4) **Wenn ACR Tasks blockiert ist**
- NICHT `az acr build` verwenden (das nutzt ACR Tasks).
- Stattdessen: `docker build` + `docker push` im GitHub Runner.

5) **Keine `||` Bash-Ketten in langen Multi-line Scripts**
- Für idempotent create/update immer `if ... then ... else ... fi`.

---

## Required GitHub Secrets

### `AZURE_CREDENTIALS` (JSON)
Erzeugen (lokal, Azure CLI):

```bash
az ad sp create-for-rbac \
  --name github-deploy-sp \
  --role Contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID> \
  --json-auth

Output komplett als GitHub Secret AZURE_CREDENTIALS speichern.

<SUBSCRIPTION_ID> ersetzen.

OPENAI_API_KEY

Als GitHub Secret speichern.

RBAC (Minimum)

Service Principal braucht i.d.R.:

Contributor auf Resource Group oder Subscription Scope

zusätzlich: AcrPush auf ACR (für docker push)

ACR Scope ID holen:

az acr show --name <ACR_NAME> --query id -o tsv

AcrPush vergeben:

az role assignment create \
  --assignee <APP_ID> \
  --role AcrPush \
  --scope <ACR_RESOURCE_ID>

APP_ID ermitteln:

az ad sp list --display-name github-deploy-sp --query "[].appId" -o tsv
Template A: Build only (Containerize only)

Use case: Nur prüfen ob Dockerfile buildet. Kein Push, kein Deploy.

name: Docker Build (CI)

on:
  push:
    branches: ["main"]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Docker build
        run: docker build -t local/azure-assistant:ci .
Template B: Build + Push to ACR (no deploy)

Use case: Image in ACR aktualisieren, Deployment separat.

name: Build and Push to ACR

on:
  push:
    branches: ["main"]

permissions:
  contents: read

jobs:
  build-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: ACR login
        run: az acr login --name <ACR_NAME>

      - name: Docker build
        run: docker build -t <ACR_NAME>.azurecr.io/<IMAGE_NAME>:latest .

      - name: Docker push
        run: docker push <ACR_NAME>.azurecr.io/<IMAGE_NAME>:latest
Template C: Build + Push + Deploy to Azure Container Apps

Use case: Vollautomatisch für MVP (empfohlen).

WICHTIG: nutzt Docker build/push (kein az acr build), damit es auch ohne ACR Tasks funktioniert.

name: Build and Deploy to Azure Container Apps

on:
  push:
    branches: ["main"]

permissions:
  contents: read

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Azure login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: ACR login
        run: az acr login --name <ACR_NAME>

      - name: Docker build
        run: docker build -t <ACR_NAME>.azurecr.io/<IMAGE_NAME>:latest .

      - name: Docker push
        run: docker push <ACR_NAME>.azurecr.io/<IMAGE_NAME>:latest

      - name: Ensure Container Apps Environment
        run: |
          if ! az containerapp env show --name <ACA_ENV> --resource-group <RG> > /dev/null 2>&1; then
            az containerapp env create --name <ACA_ENV> --resource-group <RG> --location <LOCATION>
          fi

      - name: Deploy Container App
        run: |
          if az containerapp show --name <ACA_APP> --resource-group <RG> > /dev/null 2>&1; then
            az containerapp update \
              --name <ACA_APP> \
              --resource-group <RG> \
              --image <ACR_NAME>.azurecr.io/<IMAGE_NAME>:latest \
              --set-env-vars OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
          else
            az containerapp create \
              --name <ACA_APP> \
              --resource-group <RG> \
              --environment <ACA_ENV> \
              --image <ACR_NAME>.azurecr.io/<IMAGE_NAME>:latest \
              --ingress external \
              --target-port 8501 \
              --registry-server <ACR_NAME>.azurecr.io \
              --registry-username $(az acr credential show --name <ACR_NAME> --query username -o tsv) \
              --registry-password $(az acr credential show --name <ACR_NAME> --query passwords[0].value -o tsv) \
              --env-vars OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
          fi
Common Failure Modes (Troubleshooting)
AADSTS70025 (federated identity missing)

Workflow nutzt OIDC, SP hat keine Federated Credentials.

Fix: AZURE_CREDENTIALS JSON + creds: Login.

TasksOperationsNotAllowed

az acr build oder az containerapp up nutzt ACR Tasks.

Fix: docker build + docker push im Runner.

GitHub Push Protection blocks push (secret detected)

SP secret/JSON committed.

Fix: Secret rotieren + History scrub (filter-repo/BFG) oder GitHub unblock (nur kurzfristig).

App reachable but not working

Logs check:

az containerapp logs show --name <ACA_APP> --resource-group <RG> --follow
Recommended Naming (Opinionated)

RG: rg-azure-assistant

ACR: acrassistantdemo

ACA Env: env-azure-assistant

ACA App: azure-ai-knowledge-assistant

Image: azure-assistant:latest


---

## Nächster Schritt

Commit das Runbook.

```bash
git add kb/deployment/github-actions-aca-playbook.md
git commit -m "Add CI/CD playbook for GitHub Actions + ACA"
git push