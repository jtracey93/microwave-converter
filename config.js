// Configuration for Azure AI Integration
// This file should be updated with your Azure Function URL after deployment

const CONFIG = {
    // Azure Function endpoint for scanning cooking instructions
    // Replace this with your actual Azure Function URL after deployment
    // See AZURE_AI_SETUP.md for instructions on getting this URL
    AZURE_FUNCTION_URL: '',
    
    // Feature flag to enable/disable scanning functionality
    // Set to true once Azure Function is deployed and URL is configured
    SCANNING_ENABLED: false,
    
    // Maximum image size in bytes (4MB)
    MAX_IMAGE_SIZE: 4 * 1024 * 1024,
    
    // Supported image formats
    SUPPORTED_FORMATS: ['image/jpeg', 'image/png'],
    
    // Image quality for compression (0-1)
    IMAGE_QUALITY: 0.8,
    
    // Maximum image dimensions for compression
    MAX_IMAGE_WIDTH: 1920,
    MAX_IMAGE_HEIGHT: 1920,
    
    // Wattage validation constants
    MIN_WATTAGE: 100,
    MAX_WATTAGE: 2000
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
