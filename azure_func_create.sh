RESOURCE_GROUP='mcp-petclinic'
LOCATION='swedencentral'
SA_NAME='mcppetclinicstorage'
FUNC_NAME='mcp-petclinic-func'
SUBSCRIPTION_ID='769605f1-29f2-4fd5-a384-016c3b6f1ed0'

az group create \
 --name $RESOURCE_GROUP \
 --location $LOCATION

az storage account create \
 --name $SA_NAME \
 --location $LOCATION \
 --resource-group $RESOURCE_GROUP \
 --sku Standard_LRS \
 --allow-blob-public-access false

az functionapp create \
 --resource-group $RESOURCE_GROUP \
 --name $FUNC_NAME \
 --storage-account $SA_NAME \
 --flexconsumption-location $LOCATION \
 --runtime python \
 --runtime-version 3.12


az functionapp identity assign \
 -g $RESOURCE_GROUP \
 -n $FUNC_NAME \
 --role 'Storage Blob Data Contributor' \
 --scope /subscriptions/769605f1-29f2-4fd5-a384-016c3b6f1ed0/resourcegroups/$RESOURCE_GROUP/providers/Microsoft.Storage/storageAccounts/$SA_NAME

#set storage auth to system managed identity
az functionapp deployment config set \
 --name $FUNC_NAME \
 --resource-group $RESOURCE_GROUP \
 --deployment-storage-type 'ManagedIdentity'


#set deployment settings
az functionapp config appsettings set \
--name $FUNC_NAME \
--resource-group $RESOURCE_GROUP \
--settings DEPLOYMENT_STORAGE_CONNECTION_STRING='RunFromPackage=1' AzureWebJobsStorage__accountName=$SA_NAME


#delete default storage setting
az functionapp config appsettings delete \
  --name $FUNC_NAME \
  --resource-group $RESOURCE_GROUP \
  --setting-names AzureWebJobsStorage

# Deploy the function app
rm -rf function.zip

zip -r function.zip . \
    -x "*.git*" \
    -x "*__pycache__*" \
    -x "*.pyc" \
    -x ".env*" \
    -x ".venv*" \
    -x ".vscode*" \
    -x "venv/*" \
    -x "demo_*" \
    -x "test_*" \
    -x "*.DS_Store" \
    -x "deploy.sh" \
    -x "exec.sh" \
    -x "*.md" \
    -x "Dockerfile" \
    -x ".dockerignore" \
    -x ".funcignore"


az functionapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $FUNC_NAME \
  --src function.zip
