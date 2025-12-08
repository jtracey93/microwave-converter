const { app } = require('@azure/functions');
const { ImageAnalysisClient } = require('@azure/ai-vision-image-analysis');
const { AzureKeyCredential } = require('@azure/core-auth');

/**
 * Azure Function to scan cooking instructions from images
 * Uses Azure AI Vision to extract text and parse cooking information
 */
app.http('ScanCookingInstructions', {
    methods: ['POST'],
    authLevel: 'function',
    handler: async (request, context) => {
        context.log('Processing cooking instruction image scan request');

        try {
            // Validate request
            const body = await request.json();
            
            if (!body || !body.image) {
                return {
                    status: 400,
                    jsonBody: {
                        error: 'Missing image data',
                        message: 'Request must include base64-encoded image in "image" field'
                    }
                };
            }

            // Extract base64 image data
            let imageData = body.image;
            
            // Handle data URL format (data:image/jpeg;base64,...)
            if (imageData.startsWith('data:')) {
                const base64Start = imageData.indexOf(',') + 1;
                imageData = imageData.substring(base64Start);
            }

            // Convert base64 to buffer
            const imageBuffer = Buffer.from(imageData, 'base64');

            // Validate image size (max 4MB)
            const maxSizeBytes = 4 * 1024 * 1024;
            if (imageBuffer.length > maxSizeBytes) {
                return {
                    status: 400,
                    jsonBody: {
                        error: 'Image too large',
                        message: 'Image must be less than 4MB'
                    }
                };
            }

            // Get Azure AI Vision credentials from environment
            const endpoint = process.env.AZURE_AI_VISION_ENDPOINT;
            const key = process.env.AZURE_AI_VISION_KEY;

            if (!endpoint || !key) {
                context.log.error('Missing Azure AI Vision configuration');
                return {
                    status: 500,
                    jsonBody: {
                        error: 'Configuration error',
                        message: 'AI Vision service not configured'
                    }
                };
            }

            // Create Azure AI Vision client
            const credential = new AzureKeyCredential(key);
            const client = new ImageAnalysisClient(endpoint, credential);

            // Analyze image for text using Read API
            context.log('Calling Azure AI Vision OCR...');
            const result = await client.analyzeImage(
                imageBuffer,
                {
                    features: ['Read']
                }
            );

            // Extract all text from the image
            let extractedText = '';
            if (result.readResult && result.readResult.blocks) {
                extractedText = result.readResult.blocks
                    .flatMap(block => block.lines)
                    .map(line => line.text)
                    .join(' ');
            }

            context.log(`Extracted text: ${extractedText}`);

            // Parse cooking instructions
            const cookingInfo = parseCookingInstructions(extractedText);

            // Return results
            return {
                status: 200,
                headers: {
                    'Content-Type': 'application/json'
                },
                jsonBody: {
                    success: true,
                    extractedText: extractedText,
                    ...cookingInfo
                }
            };

        } catch (error) {
            context.log.error('Error processing image:', error);
            
            return {
                status: 500,
                jsonBody: {
                    error: 'Processing failed',
                    message: error.message || 'Failed to process image'
                }
            };
        }
    }
});

/**
 * Parse cooking instructions from extracted text
 * Looks for patterns like:
 * - "800W" or "800 watts" for wattage
 * - "5:30" or "5 minutes 30 seconds" for time
 */
function parseCookingInstructions(text) {
    const result = {
        wattage: null,
        minutes: null,
        seconds: null,
        confidence: 'low'
    };

    if (!text) {
        return result;
    }

    // Normalize text
    const normalizedText = text.toLowerCase().replace(/\s+/g, ' ');

    // Parse wattage
    // Patterns: 800W, 800 W, 800 watts, 800-watt, 800watt
    const wattagePatterns = [
        /(\d{3,4})\s*w(?:att)?s?(?:\s|$|,|\.)/i,
        /(\d{3,4})\s*-?\s*watt/i,
        /power\s*:?\s*(\d{3,4})/i,
        /microwave\s*:?\s*(\d{3,4})/i
    ];

    for (const pattern of wattagePatterns) {
        const match = normalizedText.match(pattern);
        if (match) {
            const wattage = parseInt(match[1]);
            if (wattage >= 100 && wattage <= 2000) {
                result.wattage = wattage;
                break;
            }
        }
    }

    // Parse time
    // Patterns: 5:30, 5 min 30 sec, 5 minutes, 5m30s, 5'30"
    const timePatterns = [
        // Pattern: 5:30 or 05:30
        /(\d{1,2}):(\d{2})/,
        // Pattern: 5 min 30 sec or 5 minutes 30 seconds
        /(\d{1,2})\s*(?:min(?:ute)?s?)\s*(?:(?:and|&)?\s*(\d{1,2})\s*(?:sec(?:ond)?s?))?/i,
        // Pattern: 5m30s or 5m 30s
        /(\d{1,2})\s*m\s*(?:(\d{1,2})\s*s)?/i,
        // Pattern: 5'30" or 5' 30"
        /(\d{1,2})['′]\s*(?:(\d{1,2})["″])?/,
        // Pattern: just seconds (90 seconds)
        /(\d{1,3})\s*(?:sec(?:ond)?s?)/i
    ];

    for (let i = 0; i < timePatterns.length; i++) {
        const pattern = timePatterns[i];
        const match = normalizedText.match(pattern);
        
        if (match) {
            if (i === timePatterns.length - 1) {
                // Just seconds pattern
                const totalSeconds = parseInt(match[1]);
                result.minutes = Math.floor(totalSeconds / 60);
                result.seconds = totalSeconds % 60;
            } else {
                result.minutes = parseInt(match[1]) || 0;
                result.seconds = parseInt(match[2]) || 0;
            }
            
            // Validate seconds
            if (result.seconds > 59) {
                result.seconds = 59;
            }
            
            break;
        }
    }

    // Determine confidence level
    if (result.wattage && (result.minutes > 0 || result.seconds > 0)) {
        result.confidence = 'high';
    } else if (result.wattage || result.minutes > 0 || result.seconds > 0) {
        result.confidence = 'medium';
    }

    return result;
}

module.exports = { parseCookingInstructions };
