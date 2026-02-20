TITLE: Deploy Python App to Azure Container Apps

ZIEL:
Python Web App containerisieren und in Azure Container Apps deployen.

SCHRITTE:
1. Dockerfile erstellen
2. Azure Resource Group erstellen
3. Azure Container Registry erstellen
4. Image build & push
5. Container App erstellen

COMMANDS:

az group create --name rg-container-demo --location westeurope

az acr create --name acrdemo123 --resource-group rg-container-demo --sku Basic

az acr login --name acrdemo123

docker build -t acrdemo123.azurecr.io/app:v1 .

docker push acrdemo123.azurecr.io/app:v1

az containerapp create \
  --name myapp \
  --resource-group rg-container-demo \
  --image acrdemo123.azurecr.io/app:v1 \
  --target-port 8000 \
  --ingress external

VERIFY:
Browser URL der Container App öffnen.

COMMON ERRORS:
- ACR Login vergessen
- falscher Image Tag
- Port mismatch