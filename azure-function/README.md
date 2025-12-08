# Azure Function for Cooking Instructions Scanner

This Azure Function provides a secure API endpoint for scanning cooking instructions from images using Azure AI Vision.

## Features

- Accepts base64-encoded images (JPEG, PNG)
- Uses Azure AI Vision OCR to extract text
- Parses cooking instructions (wattage, time)
- Returns structured data for form auto-fill
- Secured with function-level authentication
- CORS-protected for specific domains

## Local Development

### Prerequisites

- Node.js 18+
- Azure Functions Core Tools v4
- Azure subscription (for testing with real AI Vision service)

### Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure local settings:
   
   Edit `local.settings.json` and add your Azure AI Vision credentials:
   ```json
   {
     "Values": {
       "AZURE_AI_VISION_ENDPOINT": "https://YOUR_VISION_SERVICE.cognitiveservices.azure.com/",
       "AZURE_AI_VISION_KEY": "your-api-key-here"
     }
   }
   ```

3. Start the function locally:
   ```bash
   npm start
   ```

The function will be available at:
```
http://localhost:7071/api/ScanCookingInstructions
```

### Testing Locally

Test with a sample image:

```bash
# Convert image to base64
IMAGE_BASE64=$(base64 -w 0 test-cooking-instructions.jpg)

# Call the function
curl -X POST "http://localhost:7071/api/ScanCookingInstructions" \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"data:image/jpeg;base64,$IMAGE_BASE64\"}"
```

Expected response:
```json
{
  "success": true,
  "extractedText": "Cook on 800W for 5 minutes 30 seconds",
  "wattage": 800,
  "minutes": 5,
  "seconds": 30,
  "confidence": "high"
}
```

## API Reference

### Endpoint

```
POST /api/ScanCookingInstructions
```

### Request

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

The `image` field should contain:
- Base64-encoded image data
- Optionally with data URL prefix (e.g., `data:image/jpeg;base64,`)
- Supported formats: JPEG, PNG
- Max size: 4MB

### Response

**Success (200):**
```json
{
  "success": true,
  "extractedText": "Full text extracted from the image",
  "wattage": 800,
  "minutes": 5,
  "seconds": 30,
  "confidence": "high"
}
```

**Error (400/500):**
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Confidence Levels

- `high`: Both wattage and time were found
- `medium`: Either wattage or time was found
- `low`: Neither wattage nor time could be extracted

## Text Parsing Patterns

The function recognizes various formats for cooking instructions:

### Wattage Patterns
- `800W` or `800 W`
- `800 watts` or `800-watt`
- `Power: 800`
- `Microwave: 800`

### Time Patterns
- `5:30` (minutes:seconds)
- `5 min 30 sec` or `5 minutes 30 seconds`
- `5m30s` or `5m 30s`
- `5'30"` (with prime notation)
- `90 seconds` (converts to minutes)

## Deployment

Deploy to Azure:

```bash
# Login to Azure
az login

# Deploy the function
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

See `../AZURE_AI_SETUP.md` for complete infrastructure setup instructions.

## Security

### Authentication
- Function-level auth key required (included in URL)
- Keys managed through Azure Portal or CLI

### CORS
Configure allowed origins in Function App settings:
```bash
az functionapp cors add \
  --name YOUR_FUNCTION_APP_NAME \
  --resource-group YOUR_RESOURCE_GROUP \
  --allowed-origins "https://jtracey93.github.io"
```

### Environment Variables
Never commit sensitive values. Use:
- Azure Key Vault for production (configured via app settings)
- `local.settings.json` for local development (gitignored)

## Monitoring

View logs in real-time:
```bash
func azure functionapp logstream YOUR_FUNCTION_APP_NAME
```

Or in Azure Portal:
1. Navigate to Function App
2. Go to "Monitor" → "Logs"
3. View live telemetry and errors

## Troubleshooting

### "Missing Azure AI Vision configuration"
- Verify `AZURE_AI_VISION_ENDPOINT` and `AZURE_AI_VISION_KEY` are set
- Check Key Vault integration if using managed identity

### "Image too large"
- Images must be < 4MB
- Compress the image before sending
- Consider resizing images client-side

### Poor text extraction
- Ensure good image quality (clear, well-lit)
- Text should be at least 12pt font
- Try different image formats (JPEG vs PNG)

### CORS errors
- Verify CORS settings in Function App
- Check that origin matches exactly (including protocol and port)

## Cost Optimization

- Use Azure Free Tier (5,000 vision API calls/month)
- Configure function timeout appropriately (default: 5 min)
- Consider caching results client-side
- Monitor and set up alerts for unusual usage

## Future Enhancements

Potential improvements:
- Add image preprocessing (rotation, contrast adjustment)
- Support for multiple cooking instructions in one image
- Language detection and multi-language support
- Integration with Azure Application Insights for analytics
- Caching layer with Azure Redis
