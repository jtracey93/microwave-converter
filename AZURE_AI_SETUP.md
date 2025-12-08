# Azure AI Foundry Setup Guide

This guide explains how to set up Azure AI Foundry infrastructure to enable the photo scanning feature for extracting cooking instructions.

## Overview

The photo scanning feature uses:
- **Azure AI Vision** (formerly Computer Vision) for OCR and image analysis
- **Azure Functions** as a secure backend API layer
- **Azure Key Vault** for secure credential storage
- **CORS policies** to restrict access to your web app domain only

## Architecture

```
[Web App] → [Azure Function API] → [Azure AI Vision] → [Returns extracted data]
     ↑              ↑                       ↑
     |              |                       |
  CORS Policy   API Key Auth          Managed Identity
```

## Prerequisites

- Azure subscription
- Azure CLI installed (`az` command)
- Node.js 18+ (for Azure Functions development)
- Git

## Step 1: Create Azure Resources

### 1.1 Login to Azure

```bash
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### 1.2 Create Resource Group

```bash
# Set variables
RESOURCE_GROUP="rg-microwave-converter"
LOCATION="eastus"  # Choose your preferred region

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION
```

### 1.3 Create Azure AI Vision Resource

```bash
AI_SERVICE_NAME="ai-microwave-vision"

# Create AI Vision service
az cognitiveservices account create \
  --name $AI_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --kind ComputerVision \
  --sku S1 \
  --location $LOCATION \
  --yes

# Get the endpoint
AI_ENDPOINT=$(az cognitiveservices account show \
  --name $AI_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.endpoint -o tsv)

echo "AI Vision Endpoint: $AI_ENDPOINT"
```

### 1.4 Create Storage Account (for Azure Functions)

```bash
STORAGE_ACCOUNT="stmicrowaveconv$(openssl rand -hex 4)"

az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS
```

### 1.5 Create Azure Function App

```bash
FUNCTION_APP_NAME="func-microwave-scanner"

az functionapp create \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --storage-account $STORAGE_ACCOUNT \
  --consumption-plan-location $LOCATION \
  --runtime node \
  --runtime-version 18 \
  --functions-version 4 \
  --os-type Linux
```

### 1.6 Create Key Vault for Secrets

```bash
KEY_VAULT_NAME="kv-microwave-$(openssl rand -hex 4)"

az keyvault create \
  --name $KEY_VAULT_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

## Step 2: Configure Managed Identity

Enable managed identity for the Function App to access Key Vault:

```bash
# Enable system-assigned managed identity
az functionapp identity assign \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP

# Get the principal ID
PRINCIPAL_ID=$(az functionapp identity show \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query principalId -o tsv)

# Grant Key Vault access
az keyvault set-policy \
  --name $KEY_VAULT_NAME \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list
```

## Step 3: Store Secrets in Key Vault

```bash
# Get AI Vision API key
AI_KEY=$(az cognitiveservices account keys list \
  --name $AI_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --query key1 -o tsv)

# Store in Key Vault
az keyvault secret set \
  --vault-name $KEY_VAULT_NAME \
  --name "AzureAIVisionKey" \
  --value "$AI_KEY"

az keyvault secret set \
  --vault-name $KEY_VAULT_NAME \
  --name "AzureAIVisionEndpoint" \
  --value "$AI_ENDPOINT"
```

## Step 4: Configure Function App Settings

```bash
# Configure app settings
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    "AZURE_AI_VISION_KEY=@Microsoft.KeyVault(SecretUri=https://${KEY_VAULT_NAME}.vault.azure.net/secrets/AzureAIVisionKey/)" \
    "AZURE_AI_VISION_ENDPOINT=@Microsoft.KeyVault(SecretUri=https://${KEY_VAULT_NAME}.vault.azure.net/secrets/AzureAIVisionEndpoint/)" \
    "ALLOWED_ORIGINS=https://jtracey93.github.io,http://localhost:8000"
```

## Step 5: Deploy Azure Function

The Azure Function code is located in the `azure-function/` directory. Deploy it:

```bash
cd azure-function

# Install dependencies
npm install

# Deploy to Azure
func azure functionapp publish $FUNCTION_APP_NAME
```

## Step 6: Configure CORS

```bash
# Configure CORS to only allow your website
az functionapp cors add \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --allowed-origins "https://jtracey93.github.io" "http://localhost:8000"

# Remove default wildcard if present
az functionapp cors remove \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --allowed-origins "*"
```

## Step 7: Get Function URL

```bash
# Get the function URL with key
FUNCTION_KEY=$(az functionapp function keys list \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --function-name ScanCookingInstructions \
  --query default -o tsv)

FUNCTION_URL="https://${FUNCTION_APP_NAME}.azurewebsites.net/api/ScanCookingInstructions?code=${FUNCTION_KEY}"

echo "Function URL: $FUNCTION_URL"
echo ""
echo "Add this to your web app configuration:"
echo "AZURE_FUNCTION_URL=$FUNCTION_URL"
```

## Step 8: Update Web App Configuration

Add the Function URL to your web app. For GitHub Pages:

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add new repository secret:
   - Name: `AZURE_FUNCTION_URL`
   - Value: The URL from Step 7

Update your deployment workflow to inject this during build.

## Security Features

### 1. API Key Authentication
The Azure Function requires a function-specific key in the query string, making it usable only by those who have the key.

### 2. CORS Protection
CORS is configured to only accept requests from:
- `https://jtracey93.github.io` (production)
- `http://localhost:8000` (local development)

### 3. Key Vault Integration
Sensitive credentials are stored in Azure Key Vault, not in code or environment variables.

### 4. Managed Identity
The Function App uses Managed Identity to access Key Vault, eliminating the need for credential management.

### 5. Rate Limiting
Azure Functions has built-in rate limiting (default: 200 requests per instance).

## Cost Estimation

Monthly costs for moderate usage (100 images/month):
- **Azure AI Vision**: ~$1.50/month (S1 tier, 1000 transactions)
- **Azure Functions**: ~$0.20/month (Consumption plan)
- **Storage Account**: ~$0.05/month
- **Key Vault**: ~$0.03/month

**Total: ~$1.78/month**

For free tier:
- Azure AI Vision has 5,000 free transactions/month
- Azure Functions has 1 million free executions/month

## Testing

Test the API endpoint:

```bash
# Encode an image to base64
IMAGE_BASE64=$(base64 -w 0 test-image.jpg)

# Call the API
curl -X POST "$FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"data:image/jpeg;base64,$IMAGE_BASE64\"}"
```

Expected response:
```json
{
  "wattage": 800,
  "minutes": 5,
  "seconds": 30,
  "confidence": "high",
  "extractedText": "Cook on 800W for 5:30 minutes"
}
```

## Monitoring

View logs and metrics:

```bash
# Stream function logs
func azure functionapp logstream $FUNCTION_APP_NAME

# View metrics in Azure Portal
az monitor metrics list \
  --resource "/subscriptions/.../resourceGroups/$RESOURCE_GROUP/providers/Microsoft.CognitiveServices/accounts/$AI_SERVICE_NAME" \
  --metric "ProcessedImages"
```

## Troubleshooting

### Issue: CORS errors in browser console

**Solution**: Verify CORS settings:
```bash
az functionapp cors show --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP
```

### Issue: 401 Unauthorized error

**Solution**: Check if the function key is correct or if Managed Identity has Key Vault access.

### Issue: AI Vision returns no text

**Solution**: Ensure the image is:
- Clear and well-lit
- Text is at least 12pt font size
- Image is in JPEG or PNG format
- Less than 4MB in size

## Cleanup

To remove all resources:

```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## Next Steps

1. Deploy the Azure Function code (see `azure-function/README.md`)
2. Test the integration locally
3. Update the web app with the Function URL
4. Monitor usage and adjust pricing tiers as needed
5. Consider adding Application Insights for better monitoring

## References

- [Azure AI Vision Documentation](https://learn.microsoft.com/azure/cognitive-services/computer-vision/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)
- [Azure Key Vault Documentation](https://learn.microsoft.com/azure/key-vault/)
