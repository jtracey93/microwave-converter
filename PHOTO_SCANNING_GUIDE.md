# Photo Scanning Usage Guide

This guide demonstrates how to use the AI-powered photo scanning feature to extract cooking instructions from images.

## Overview

The photo scanning feature allows you to take a picture of cooking instructions (from food packaging, recipe books, etc.) and automatically extract:
- Microwave wattage (e.g., 800W, 1000W)
- Cooking time (minutes and seconds)

## How to Use

### Method 1: Take a Photo

1. Click the "📸 Take Photo" button
2. Allow camera access when prompted by your browser
3. Point your camera at the cooking instructions
4. Take the photo
5. The app will automatically:
   - Extract text from the image using Azure AI Vision
   - Parse wattage and cooking time
   - Fill in the form fields
6. Verify the extracted values and click "Calculate"

### Method 2: Upload an Image

1. Click the "🖼️ Upload Image" button
2. Select an image file from your device (JPEG or PNG)
3. The app will process the image and auto-fill the form
4. Verify the values and click "Calculate"

## Tips for Best Results

### Photo Quality
- **Good lighting**: Take photos in well-lit areas
- **Clear text**: Ensure the text is in focus and legible
- **Straight angle**: Try to photograph the instructions straight-on (not at an angle)
- **Close-up**: Get close enough so the text fills most of the frame

### Text Requirements
- Text should be at least 12pt font size
- Black text on white/light background works best
- Printed text is easier to read than handwritten

### Common Patterns Recognized

The AI can recognize various formats:

**Wattage:**
- "800W" or "800 W"
- "800 watts" or "800-watt"
- "Power: 800"
- "Microwave: 800"

**Time:**
- "5:30" (5 minutes 30 seconds)
- "5 min 30 sec"
- "5 minutes 30 seconds"
- "5m30s" or "5m 30s"
- "5'30"" (with prime notation)
- "90 seconds" (converts to 1m 30s)

## Examples

### Example 1: Simple Cooking Instructions
```
Cook on 800W for 5:30 minutes
```
**Extracted:**
- Wattage: 800W
- Time: 5 minutes 30 seconds

### Example 2: Detailed Instructions
```
Microwave Instructions:
Power Level: 1000 watts
Cooking Time: 3 minutes
Stir halfway through
```
**Extracted:**
- Wattage: 1000W
- Time: 3 minutes 0 seconds

### Example 3: Compact Format
```
800W | 2m 45s
```
**Extracted:**
- Wattage: 800W
- Time: 2 minutes 45 seconds

## Confidence Levels

The app provides feedback on detection confidence:

- **High Confidence**: Both wattage and time were clearly detected
- **Medium Confidence**: Either wattage or time was detected
- **Low Confidence**: Partial or uncertain information

Always verify the extracted values, especially for medium/low confidence results.

## Troubleshooting

### "No cooking instructions found"
**Causes:**
- Image is blurry or out of focus
- Text is too small
- Poor lighting
- Text is handwritten or stylized font

**Solutions:**
- Retake the photo with better lighting
- Get closer to the text
- Try a different angle
- Use the manual entry option instead

### "Image too large"
**Cause:** Image file exceeds 4MB

**Solutions:**
- The app automatically compresses images, but very large files might fail
- Reduce image resolution before uploading
- Take a new photo at lower resolution

### Scanner buttons are disabled
**Cause:** Azure AI integration not configured

**Solution:**
- This is normal if you haven't set up the Azure infrastructure
- Follow the setup guide in `AZURE_AI_SETUP.md`
- The app works perfectly fine with manual entry

### Incorrect values extracted
**Causes:**
- Complex layouts with multiple cooking options
- Multiple wattages or times listed
- Ambiguous text

**Solutions:**
- Manually correct the extracted values
- The AI picks the first clearly identifiable values
- Use manual entry if the photo isn't clear

## Privacy & Security

### Data Handling
- Images are sent to Azure AI Vision for processing
- Images are **not stored** anywhere
- Only extracted text is temporarily kept for parsing
- No user data or images are saved on servers

### Security Features
- Communication uses HTTPS encryption
- Azure Function endpoint is protected with API keys
- CORS policies restrict access to authorized domains only
- API calls are rate-limited to prevent abuse

## Feature Availability

The photo scanning feature is **optional** and requires:
- Azure subscription
- Deployed Azure Function
- Configured Azure AI Vision service

See `AZURE_AI_SETUP.md` for setup instructions.

If not configured, the buttons will be disabled and you can use manual entry instead.

## Cost Considerations

When using Azure AI:
- Free tier: 5,000 transactions/month
- S1 tier: ~$1/1000 transactions
- Azure Functions: Free tier includes 1M executions/month

For personal use, the free tier is usually sufficient.

## Accessibility

- Works on desktop and mobile devices
- Compatible with screen readers
- Keyboard navigation supported
- Touch-friendly interface on mobile

## Browser Support

Requires modern browsers:
- Chrome/Edge 90+
- Safari 14+
- Firefox 88+

Camera access requires HTTPS in production (works with localhost in development).
