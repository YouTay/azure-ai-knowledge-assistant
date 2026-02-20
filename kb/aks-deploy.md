TITLE: Deploy App to Azure Kubernetes Service (AKS)

ZIEL:
Containerisierte App in AKS deployen.

SCHRITTE:
1. Resource Group erstellen
2. AKS Cluster erstellen
3. ACR erstellen + attach
4. Image pushen
5. Deployment YAML anwenden

COMMANDS:

az group create --name rg-aks-demo --location westeurope

az acr create --name acraksdemo --resource-group rg-aks-demo --sku Basic

az aks create \
  --name aks-demo \
  --resource-group rg-aks-demo \
  --node-count 1 \
  --attach-acr acraksdemo \
  --generate-ssh-keys

az aks get-credentials --name aks-demo --resource-group rg-aks-demo

kubectl apply -f deployment.yaml

VERIFY:
kubectl get pods
kubectl get svc

COMMON ERRORS:
- ACR nicht attached
- falscher kube context
- ImagePullBackOff