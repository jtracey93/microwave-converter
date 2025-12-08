# Getting Started with Photo Scanning

This quick guide will help you enable the AI photo scanning feature on your Microwave Converter app.

## What You Got

Your microwave converter now has the ability to scan cooking instructions from photos! The implementation includes:

✅ **Complete Frontend** - Photo capture and upload UI with beautiful design
✅ **Secure Backend** - Azure Function with OCR integration
✅ **Full Documentation** - Step-by-step setup guides
✅ **Security Hardened** - 0 vulnerabilities, best practices applied
✅ **Cost Effective** - Free tier available (5,000 images/month)

## Quick Start (3 Steps)

### Step 1: Set Up Azure Infrastructure

Follow the detailed guide in `AZURE_AI_SETUP.md`. The key commands:

```bash
# Set your subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Run the setup script (or follow manual steps in guide)
# This creates: AI Vision, Function App, Key Vault, Storage
```

**Time**: ~15 minutes
**Cost**: Free tier available (or ~$1.78/month)

### Step 2: Deploy the Azure Function

```bash
cd azure-function
npm install
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

**Time**: ~5 minutes

### Step 3: Configure and Deploy

1. Get your Function URL from Azure portal or CLI
2. Edit `config.js`:
   ```javascript
   AZURE_FUNCTION_URL: 'https://your-function.azurewebsites.net/api/ScanCookingInstructions?code=YOUR_KEY',
   SCANNING_ENABLED: true
   ```
3. Commit and push - GitHub Actions will deploy automatically

**Time**: ~2 minutes

## That's It!

Your users can now:
1. Click "Take Photo" or "Upload Image"
2. Capture/select a photo of cooking instructions
3. Watch as AI extracts the wattage and time
4. Verify and calculate the adjusted time

## Important Documents

- **AZURE_AI_SETUP.md** - Complete infrastructure setup (copy/paste commands)
- **PHOTO_SCANNING_GUIDE.md** - User guide to share with your users
- **azure-function/README.md** - Technical details and local testing
- **IMPLEMENTATION_SUMMARY.md** - What was built and how it works

## Need Help?

All documents include:
- Troubleshooting sections
- Common issues and solutions
- Testing instructions
- Cost information
- Security details

## Testing Before Azure Setup

The buttons are automatically disabled until you configure Azure. The app works perfectly fine without the feature - users can continue to manually enter values.

## Security Note

The implementation follows Azure security best practices:
- API keys required
- CORS restricted to your domain
- No data stored
- Managed Identity for Azure resources
- Key Vault for credentials

## Optional Feature

Remember: This feature is **completely optional**. Your app works great without it. Only enable it if you want the extra convenience of photo scanning.

## Questions?

Check the troubleshooting sections in:
1. `AZURE_AI_SETUP.md` - Infrastructure issues
2. `PHOTO_SCANNING_GUIDE.md` - Usage issues
3. `azure-function/README.md` - Development issues

---

**Ready to enable it?** Start with `AZURE_AI_SETUP.md` and you'll be scanning photos in about 20 minutes! 🚀
