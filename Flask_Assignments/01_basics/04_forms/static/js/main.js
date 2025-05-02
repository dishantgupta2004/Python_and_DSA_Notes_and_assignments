// static/js/main.js

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle flash message close buttons
    const closeButtons = document.querySelectorAll('.flash-message .close-btn');
    
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(message => {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s ease';
            
            setTimeout(function() {
                message.style.display = 'none';
            }, 500);
        });
    }, 5000);
    
    // Validate form inputs in real-time
    const formInputs = document.querySelectorAll('.form-control');
    
    formInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });
    
    // Registration form validation
    const registrationForm = document.querySelector('.registration-form form');
    
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate all inputs
            formInputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });
            
            // Check terms agreement
            const termsCheckbox = document.querySelector('input[name="terms"]');
            if (termsCheckbox && !termsCheckbox.checked) {
                const errorMessage = termsCheckbox.parentElement.nextElementSibling || document.createElement('div');
                
                if (!errorMessage.classList.contains('error-message')) {
                    errorMessage.className = 'error-message';
                    termsCheckbox.parentElement.parentElement.appendChild(errorMessage);
                }
                
                errorMessage.textContent = 'You must agree to the terms and conditions';
                isValid = false;
            }
            
            if (!isValid) {
                event.preventDefault();
                // Scroll to the first error
                const firstError = document.querySelector('.error-message');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    }
    
    // Tab switcher for user profile
    const tabs = document.querySelectorAll('.tab');
    
    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Get the tab ID
                const tabId = this.getAttribute('data-tab');
                
                // Hide all tab contents
                const tabContents = document.querySelectorAll('.tab-content');
                tabContents.forEach(content => {
                    content.classList.add('hidden');
                });
                
                // Show the selected tab content
                document.getElementById(`${tabId}-content`).classList.remove('hidden');
            });
        });
    }
    
    // Character counter for textarea
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        // Create counter element
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        counter.textContent = '0/' + (textarea.getAttribute('maxlength') || '500');
        
        // Insert counter after textarea
        textarea.parentNode.insertBefore(counter, textarea.nextSibling);
        
        // Update counter on input
        textarea.addEventListener('input', function() {
            const count = this.value.length;
            const max = this.getAttribute('maxlength') || 500;
            
            counter.textContent = count + '/' + max;
            
            if (count > max * 0.9) {
                counter.style.color = '#b00020';
            } else {
                counter.style.color = '#757575';
            }
        });
    });
    
    // Helper function to validate inputs
    function validateInput(input) {
        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';
        
        // Get the error message element or create one
        const errorElement = input.nextElementSibling && input.nextElementSibling.classList.contains('error-message') ?
            input.nextElementSibling : document.createElement('div');
        
        if (!errorElement.classList.contains('error-message')) {
            errorElement.className = 'error-message';
            input.parentNode.insertBefore(errorElement, input.nextSibling);
        }
        
        // Required field validation
        if (input.hasAttribute('required') && value === '') {
            isValid = false;
            errorMessage = 'This field is required';
        }
        // Email validation
        else if (input.type === 'email' && value !== '') {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
        }
        // Phone validation
        else if (input.name === 'phone' && value !== '') {
            const phonePattern = /^\+?[0-9]{10,15}$/;
            if (!phonePattern.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid phone number';
            }
        }
        // Text length validation for textarea
        else if (input.tagName.toLowerCase() === 'textarea') {
            const minLength = parseInt(input.getAttribute('minlength') || '0');
            const maxLength = parseInt(input.getAttribute('maxlength') || '500');
            
            if (value.length < minLength) {
                isValid = false;
                errorMessage = `Please write at least ${minLength} characters`;
            } else if (value.length > maxLength) {
                isValid = false;
                errorMessage = `Please write no more than ${maxLength} characters`;
            }
        }
        
        // Update UI based on validation
        if (!isValid) {
            errorElement.textContent = errorMessage;
            input.classList.add('is-invalid');
        } else {
            errorElement.textContent = '';
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
        
        return isValid;
    }
});