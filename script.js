// Microwave Time Converter JavaScript
class MicrowaveConverter {
    constructor() {
        this.form = document.getElementById('converterForm');
        this.resultSection = document.getElementById('result');
        this.resultTime = document.getElementById('resultTime');
        this.resultExplanation = document.getElementById('resultExplanation');
        this.resetBtn = document.getElementById('resetBtn');
        
        // Photo scanner elements
        this.capturePhotoBtn = document.getElementById('capturePhotoBtn');
        this.uploadPhotoBtn = document.getElementById('uploadPhotoBtn');
        this.photoInput = document.getElementById('photoInput');
        this.uploadInput = document.getElementById('uploadInput');
        this.scanStatus = document.getElementById('scanStatus');
        this.scanResult = document.getElementById('scanResult');
        this.scanResultText = document.getElementById('scanResultText');
        
        this.init();
    }

    init() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        this.resetBtn.addEventListener('click', this.resetForm.bind(this));
        
        // Add real-time validation
        this.addInputValidation();
        
        // Add number input formatting
        this.addInputFormatting();
        
        // Add increment/decrement button handlers
        this.addControlButtons();
        
        // Add photo scanner handlers
        this.addPhotoScannerHandlers();
    }

    addPhotoScannerHandlers() {
        // Check if scanning is enabled
        if (!CONFIG.SCANNING_ENABLED || !CONFIG.AZURE_FUNCTION_URL) {
            // Disable scanner buttons if not configured
            this.capturePhotoBtn.disabled = true;
            this.uploadPhotoBtn.disabled = true;
            this.capturePhotoBtn.title = 'Photo scanning not configured. See AZURE_AI_SETUP.md';
            this.uploadPhotoBtn.title = 'Photo scanning not configured. See AZURE_AI_SETUP.md';
            this.capturePhotoBtn.style.opacity = '0.5';
            this.uploadPhotoBtn.style.opacity = '0.5';
            this.capturePhotoBtn.style.cursor = 'not-allowed';
            this.uploadPhotoBtn.style.cursor = 'not-allowed';
            return;
        }

        // Take photo button
        this.capturePhotoBtn.addEventListener('click', () => {
            this.photoInput.click();
        });

        // Upload photo button
        this.uploadPhotoBtn.addEventListener('click', () => {
            this.uploadInput.click();
        });

        // Handle photo capture
        this.photoInput.addEventListener('change', (e) => {
            this.handlePhotoSelected(e.target.files[0]);
        });

        // Handle photo upload
        this.uploadInput.addEventListener('change', (e) => {
            this.handlePhotoSelected(e.target.files[0]);
        });
    }

    addInputValidation() {
        const inputs = this.form.querySelectorAll('input[type="number"]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateInput(input));
            input.addEventListener('input', () => this.clearErrors(input));
        });
    }

    addInputFormatting() {
        // Format number inputs to prevent invalid values
        const wattageInputs = ['originalWattage', 'targetWattage'];
        const timeInputs = ['originalMinutes', 'originalSeconds'];

        wattageInputs.forEach(id => {
            const input = document.getElementById(id);
            input.addEventListener('input', (e) => {
                let value = parseInt(e.target.value);
                if (value > 2000) e.target.value = 2000;
                if (value < 0) e.target.value = '';
            });
        });

        // Prevent seconds from going over 59
        document.getElementById('originalSeconds').addEventListener('input', (e) => {
            let value = parseInt(e.target.value);
            if (value > 59) e.target.value = 59;
            if (value < 0) e.target.value = 0;
        });

        // Prevent minutes from going over reasonable limits
        document.getElementById('originalMinutes').addEventListener('input', (e) => {
            let value = parseInt(e.target.value);
            if (value > 60) e.target.value = 60;
            if (value < 0) e.target.value = 0;
        });
    }

    addControlButtons() {
        // Wattage controls - increment/decrement by 100
        document.getElementById('originalWattageUp').addEventListener('click', () => {
            this.adjustValue('originalWattage', 100);
        });
        document.getElementById('originalWattageDown').addEventListener('click', () => {
            this.adjustValue('originalWattage', -100);
        });
        document.getElementById('targetWattageUp').addEventListener('click', () => {
            this.adjustValue('targetWattage', 100);
        });
        document.getElementById('targetWattageDown').addEventListener('click', () => {
            this.adjustValue('targetWattage', -100);
        });

        // Time controls - minutes by 1, seconds by 10
        document.getElementById('minutesUp').addEventListener('click', () => {
            this.adjustValue('originalMinutes', 1);
        });
        document.getElementById('minutesDown').addEventListener('click', () => {
            this.adjustValue('originalMinutes', -1);
        });
        document.getElementById('secondsUp').addEventListener('click', () => {
            this.adjustValue('originalSeconds', 10);
        });
        document.getElementById('secondsDown').addEventListener('click', () => {
            this.adjustValue('originalSeconds', -10);
        });
    }

    adjustValue(inputId, delta) {
        const input = document.getElementById(inputId);
        let currentValue = parseInt(input.value, 10) || 0;
        let newValue = currentValue + delta;
        
        // Apply constraints
        const min = parseInt(input.getAttribute('min'), 10) || 0;
        const max = parseInt(input.getAttribute('max'), 10) || Infinity;
        
        newValue = Math.max(min, Math.min(max, newValue));
        input.value = newValue;
        
        // Trigger validation
        this.clearErrors(input);
    }

    validateInput(input) {
        const value = parseFloat(input.value);
        const fieldGroup = input.closest('.input-group') || input.closest('.form-group');
        
        this.clearErrors(input);

        if (input.hasAttribute('required') && (!input.value || value <= 0)) {
            this.showError(fieldGroup, 'This field is required');
            return false;
        }

        if (input.id.includes('Wattage')) {
            if (value < 100) {
                this.showError(fieldGroup, 'Wattage must be at least 100 watts');
                return false;
            }
            if (value > 2000) {
                this.showError(fieldGroup, 'Wattage must be 2000 watts or less');
                return false;
            }
        }

        if (input.id === 'originalSeconds' && value > 59) {
            this.showError(fieldGroup, 'Seconds must be between 0-59');
            return false;
        }

        if (input.id === 'originalMinutes' && value > 60) {
            this.showError(fieldGroup, 'Minutes should be reasonable (≤60)');
            return false;
        }

        this.showSuccess(fieldGroup);
        return true;
    }

    showError(fieldGroup, message) {
        fieldGroup.classList.add('error');
        fieldGroup.classList.remove('success');
        
        let errorMsg = fieldGroup.querySelector('.error-message');
        if (!errorMsg) {
            errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            fieldGroup.appendChild(errorMsg);
        }
        errorMsg.textContent = message;
    }

    showSuccess(fieldGroup) {
        fieldGroup.classList.add('success');
        fieldGroup.classList.remove('error');
        
        const errorMsg = fieldGroup.querySelector('.error-message');
        if (errorMsg) {
            errorMsg.remove();
        }
    }

    clearErrors(input) {
        const fieldGroup = input.closest('.input-group') || input.closest('.form-group');
        fieldGroup.classList.remove('error', 'success');
        
        const errorMsg = fieldGroup.querySelector('.error-message');
        if (errorMsg) {
            errorMsg.remove();
        }
    }

    handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            this.showFormErrors();
            return;
        }

        const formData = this.getFormData();
        const result = this.calculateConversion(formData);
        this.displayResult(result, formData);
    }

    validateForm() {
        const inputs = this.form.querySelectorAll('input[type="number"]');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateInput(input)) {
                isValid = false;
            }
        });

        // Check if at least some time is specified
        const minutes = parseInt(document.getElementById('originalMinutes').value) || 0;
        const seconds = parseInt(document.getElementById('originalSeconds').value) || 0;
        
        if (minutes === 0 && seconds === 0) {
            const timeGroup = document.querySelector('.time-row');
            this.showError(timeGroup, 'Please specify at least some cooking time');
            isValid = false;
        }

        return isValid;
    }

    showFormErrors() {
        // Scroll to first error
        const firstError = this.form.querySelector('.input-group.error, .form-group.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    getFormData() {
        return {
            originalWattage: parseInt(document.getElementById('originalWattage').value),
            originalMinutes: parseInt(document.getElementById('originalMinutes').value) || 0,
            originalSeconds: parseInt(document.getElementById('originalSeconds').value) || 0,
            targetWattage: parseInt(document.getElementById('targetWattage').value)
        };
    }

    calculateConversion(data) {
        // Convert original time to total seconds
        const originalTotalSeconds = (data.originalMinutes * 60) + data.originalSeconds;
        
        // Apply the conversion formula:
        // New Time = (Original Time × Recipe Wattage) ÷ Your Wattage
        const newTotalSeconds = Math.round((originalTotalSeconds * data.originalWattage) / data.targetWattage);
        
        // Convert back to minutes and seconds
        const newMinutes = Math.floor(newTotalSeconds / 60);
        const newSeconds = newTotalSeconds % 60;
        
        return {
            originalTotalSeconds,
            newTotalSeconds,
            newMinutes,
            newSeconds,
            ratio: data.originalWattage / data.targetWattage
        };
    }

    displayResult(result, formData) {
        // Format the time display
        let timeString = '';
        if (result.newMinutes > 0) {
            timeString += `${result.newMinutes}m `;
        }
        timeString += `${result.newSeconds}s`;
        
        this.resultTime.textContent = timeString;
        
        // Simple explanation
        const originalTimeStr = this.formatTime(formData.originalMinutes, formData.originalSeconds);
        let explanation = `Cook for ${timeString} instead of ${originalTimeStr}`;
        
        this.resultExplanation.textContent = explanation;
        
        // Show result
        this.resultSection.classList.remove('hidden');
        this.resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Add analytics event (if you have analytics setup)
        this.trackConversion(formData, result);
    }

    formatTime(minutes, seconds) {
        let timeStr = '';
        if (minutes > 0) {
            timeStr += `${minutes}m `;
        }
        if (seconds > 0 || minutes === 0) {
            timeStr += `${seconds}s`;
        }
        return timeStr.trim();
    }

    resetForm() {
        this.form.reset();
        
        // Set default values
        document.getElementById('originalWattage').value = 800;
        document.getElementById('targetWattage').value = 700;
        document.getElementById('originalMinutes').value = 8;
        document.getElementById('originalSeconds').value = 0;
        
        this.resultSection.classList.add('hidden');
        
        // Clear all validation states
        const formGroups = this.form.querySelectorAll('.input-group, .form-group');
        formGroups.forEach(group => {
            group.classList.remove('error', 'success');
            const errorMsg = group.querySelector('.error-message');
            if (errorMsg) {
                errorMsg.remove();
            }
        });
        
        // Focus on first input
        document.getElementById('originalWattage').focus();
        
        // Scroll to top
        this.form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    trackConversion(formData, result) {
        // This is where you could add analytics tracking
        // For example, Google Analytics, Adobe Analytics, etc.
        console.log('Conversion calculated:', {
            originalWattage: formData.originalWattage,
            targetWattage: formData.targetWattage,
            originalTime: formData.originalMinutes * 60 + formData.originalSeconds,
            newTime: result.newTotalSeconds,
            ratio: result.ratio
        });
    }

    // Photo Scanner Methods
    async handlePhotoSelected(file) {
        if (!file) return;

        // Validate file type
        if (!CONFIG.SUPPORTED_FORMATS.includes(file.type)) {
            this.showScanError('Please select a valid image file (JPEG or PNG)');
            return;
        }

        // Validate file size
        if (file.size > CONFIG.MAX_IMAGE_SIZE) {
            this.showScanError('Image is too large. Please choose an image smaller than 4MB.');
            return;
        }

        try {
            // Show loading state
            this.showScanStatus('Scanning image...');

            // Compress and convert image to base64
            const base64Image = await this.processImage(file);

            // Send to Azure Function for analysis
            const result = await this.scanCookingInstructions(base64Image);

            // Process and display results
            this.handleScanResult(result);

        } catch (error) {
            console.error('Error scanning image:', error);
            this.showScanError(error.message || 'Failed to scan image. Please try again.');
        } finally {
            // Reset file inputs
            this.photoInput.value = '';
            this.uploadInput.value = '';
        }
    }

    async processImage(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                const img = new Image();
                
                img.onload = () => {
                    // Create canvas for image processing
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    // Calculate new dimensions (if needed)
                    let width = img.width;
                    let height = img.height;
                    
                    if (width > CONFIG.MAX_IMAGE_WIDTH || height > CONFIG.MAX_IMAGE_HEIGHT) {
                        const ratio = Math.min(
                            CONFIG.MAX_IMAGE_WIDTH / width,
                            CONFIG.MAX_IMAGE_HEIGHT / height
                        );
                        width = width * ratio;
                        height = height * ratio;
                    }
                    
                    canvas.width = width;
                    canvas.height = height;
                    
                    // Draw and compress image
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    // Convert to base64
                    const base64 = canvas.toDataURL('image/jpeg', CONFIG.IMAGE_QUALITY);
                    resolve(base64);
                };
                
                img.onerror = () => {
                    reject(new Error('Failed to load image'));
                };
                
                img.src = e.target.result;
            };
            
            reader.onerror = () => {
                reject(new Error('Failed to read image file'));
            };
            
            reader.readAsDataURL(file);
        });
    }

    async scanCookingInstructions(base64Image) {
        const response = await fetch(CONFIG.AZURE_FUNCTION_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: base64Image
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || 'Failed to scan image');
        }

        return await response.json();
    }

    handleScanResult(result) {
        if (!result.success) {
            this.showScanError('Could not extract cooking instructions from the image.');
            return;
        }

        const { wattage, minutes, seconds, confidence, extractedText } = result;

        // Check if we got any useful data
        if (!wattage && !minutes && !seconds) {
            this.showScanError('No cooking instructions found in the image. Please try a clearer photo.');
            return;
        }

        // Auto-fill form fields
        if (wattage && wattage >= 100 && wattage <= 2000) {
            document.getElementById('originalWattage').value = wattage;
        }
        
        if (minutes !== null && minutes >= 0) {
            document.getElementById('originalMinutes').value = minutes;
        }
        
        if (seconds !== null && seconds >= 0 && seconds <= 59) {
            document.getElementById('originalSeconds').value = seconds;
        }

        // Show success message
        let resultMessage = 'Successfully scanned! ';
        const foundItems = [];
        
        if (wattage) foundItems.push(`${wattage}W`);
        if (minutes > 0 || seconds > 0) {
            foundItems.push(this.formatTime(minutes || 0, seconds || 0));
        }
        
        if (foundItems.length > 0) {
            resultMessage += `Found: ${foundItems.join(', ')}`;
        } else {
            resultMessage += 'Partial information detected. Please verify the values.';
        }

        if (confidence === 'low' || confidence === 'medium') {
            resultMessage += ' Please verify the values are correct.';
        }

        this.showScanSuccess(resultMessage, extractedText);

        // Clear any result from previous calculations
        this.resultSection.classList.add('hidden');
    }

    showScanStatus(message) {
        this.scanResult.classList.add('hidden');
        this.scanStatus.classList.remove('hidden');
        this.scanStatus.querySelector('.scan-text').textContent = message;
    }

    showScanSuccess(message, extractedText) {
        this.scanStatus.classList.add('hidden');
        this.scanResult.classList.remove('hidden');
        
        let detailsHtml = `<strong>${message}</strong>`;
        if (extractedText) {
            detailsHtml += `<br><small style="color: #666;">Detected text: "${extractedText.substring(0, 100)}${extractedText.length > 100 ? '...' : ''}"</small>`;
        }
        
        this.scanResultText.innerHTML = detailsHtml;

        // Auto-hide success message after 5 seconds
        setTimeout(() => {
            this.scanResult.classList.add('hidden');
        }, 5000);
    }

    showScanError(message) {
        this.scanStatus.classList.add('hidden');
        this.scanResult.classList.remove('hidden');
        this.scanResult.style.background = 'linear-gradient(135deg, #ffe0e0 0%, #ffd4d4 100%)';
        this.scanResult.style.borderColor = '#dc3545';
        
        this.scanResultText.innerHTML = `<strong style="color: #721c24;">⚠️ ${message}</strong>`;
        
        // Reset styles after 5 seconds
        setTimeout(() => {
            this.scanResult.classList.add('hidden');
            this.scanResult.style.background = '';
            this.scanResult.style.borderColor = '';
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the converter
    new MicrowaveConverter();
    
    // Add service worker for PWA capabilities (optional)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js').catch(console.error);
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Enter key to calculate (when form has focus)
        if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
            e.preventDefault();
            document.querySelector('.calculate-btn').click();
        }
        
        // Escape key to reset
        if (e.key === 'Escape') {
            const resetBtn = document.getElementById('resetBtn');
            if (!resetBtn.closest('.result-section').classList.contains('hidden')) {
                resetBtn.click();
            }
        }
    });
});

// Utility functions for potential future enhancements
const Utils = {
    // Format cooking time in a human-readable way
    formatCookingTime(totalSeconds) {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;
        
        let formatted = '';
        if (hours > 0) formatted += `${hours}h `;
        if (minutes > 0) formatted += `${minutes}m `;
        if (seconds > 0 || (hours === 0 && minutes === 0)) formatted += `${seconds}s`;
        
        return formatted.trim();
    },
    
    // Validate microwave wattage
    isValidWattage(wattage) {
        return wattage >= 100 && wattage <= 2000;
    },
    
    // Get power level recommendations
    getPowerLevelRecommendation(originalWattage, targetWattage) {
        const ratio = originalWattage / targetWattage;
        
        if (ratio > 1.5) {
            return {
                powerLevel: '70-80%',
                reason: 'Your microwave is much more powerful. Consider using a lower power level.'
            };
        } else if (ratio < 0.7) {
            return {
                powerLevel: '100%',
                reason: 'Your microwave is less powerful. Use full power and check frequently.'
            };
        }
        
        return {
            powerLevel: '100%',
            reason: 'Your microwave power is similar to the recipe. Use normal power.'
        };
    }
};
