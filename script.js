// Microwave Time Converter JavaScript
class MicrowaveConverter {
    constructor() {
        this.form = document.getElementById('converterForm');
        this.resultSection = document.getElementById('result');
        this.resultTime = document.getElementById('resultTime');
        this.resultExplanation = document.getElementById('resultExplanation');
        this.resetBtn = document.getElementById('resetBtn');
        
        this.init();
    }

    init() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        this.resetBtn.addEventListener('click', this.resetForm.bind(this));
        
        // Add real-time validation
        this.addInputValidation();
        
        // Add number input formatting
        this.addInputFormatting();
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
        document.getElementById('targetWattage').value = 700;
        document.getElementById('originalMinutes').value = 0;
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
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the converter
    new MicrowaveConverter();
    
    // Add quick select functionality
    addQuickSelectButtons();
    
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

// Quick select functionality
function addQuickSelectButtons() {
    const commonWattages = [600, 700, 800, 900, 1000, 1100, 1200];
    
    // Add quick select for original wattage
    const originalContainer = document.getElementById('originalWattageQuick');
    commonWattages.forEach(wattage => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'quick-select-btn';
        btn.textContent = `${wattage}W`;
        btn.addEventListener('click', () => {
            document.getElementById('originalWattage').value = wattage;
        });
        originalContainer.appendChild(btn);
    });
    
    // Add quick select for target wattage
    const targetContainer = document.getElementById('targetWattageQuick');
    commonWattages.forEach(wattage => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'quick-select-btn';
        btn.textContent = `${wattage}W`;
        btn.addEventListener('click', () => {
            document.getElementById('targetWattage').value = wattage;
        });
        targetContainer.appendChild(btn);
    });
    
    // Add quick select for common cooking times
    const timeContainer = document.getElementById('timeQuickSelect');
    const commonTimes = [
        { label: '30s', minutes: 0, seconds: 30 },
        { label: '1m', minutes: 1, seconds: 0 },
        { label: '1m 30s', minutes: 1, seconds: 30 },
        { label: '2m', minutes: 2, seconds: 0 },
        { label: '2m 30s', minutes: 2, seconds: 30 },
        { label: '3m', minutes: 3, seconds: 0 },
        { label: '4m', minutes: 4, seconds: 0 },
        { label: '5m', minutes: 5, seconds: 0 },
        { label: '7m', minutes: 7, seconds: 0 },
        { label: '8m', minutes: 8, seconds: 0 },
        { label: '10m', minutes: 10, seconds: 0 }
    ];
    
    commonTimes.forEach(time => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'quick-select-btn time-btn';
        btn.textContent = time.label;
        btn.addEventListener('click', () => {
            document.getElementById('originalMinutes').value = time.minutes;
            document.getElementById('originalSeconds').value = time.seconds;
        });
        timeContainer.appendChild(btn);
    });
}

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
