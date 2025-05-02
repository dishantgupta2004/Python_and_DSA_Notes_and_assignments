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
    
    // Tab switcher for user profile and history page
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
    
    // Password confirmation validation
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    
    if (passwordField && confirmPasswordField) {
        confirmPasswordField.addEventListener('input', function() {
            if (this.value !== passwordField.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
        
        passwordField.addEventListener('input', function() {
            if (confirmPasswordField.value !== '' && confirmPasswordField.value !== this.value) {
                confirmPasswordField.setCustomValidity('Passwords do not match');
            } else {
                confirmPasswordField.setCustomValidity('');
            }
        });
    }
    
    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    
                    // Create or update error message
                    let errorMessage = field.nextElementSibling;
                    
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('div');
                        errorMessage.className = 'error-message';
                        field.parentNode.insertBefore(errorMessage, field.nextElementSibling);
                    }
                    
                    errorMessage.textContent = 'This field is required';
                    
                    // Highlight the field
                    field.classList.add('invalid');
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
        
        // Live validation as user types
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateInput(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('invalid')) {
                    validateInput(this);
                }
            });
        });
    });
    
    // Helper function to validate inputs
    function validateInput(input) {
        // Skip validation for non-required empty fields
        if (!input.hasAttribute('required') && !input.value.trim()) {
            // Remove any existing error message
            const errorMessage = input.nextElementSibling;
            if (errorMessage && errorMessage.classList.contains('error-message')) {
                errorMessage.textContent = '';
            }
            
            input.classList.remove('invalid');
            return true;
        }
        
        // Required field validation
        if (input.hasAttribute('required') && !input.value.trim()) {
            // Create or update error message
            let errorMessage = input.nextElementSibling;
            
            if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                input.parentNode.insertBefore(errorMessage, input.nextElementSibling);
            }
            
            errorMessage.textContent = 'This field is required';
            input.classList.add('invalid');
            return false;
        }
        
        // Email validation
        if (input.type === 'email' && input.value.trim()) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (!emailPattern.test(input.value.trim())) {
                let errorMessage = input.nextElementSibling;
                
                if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                    errorMessage = document.createElement('div');
                    errorMessage.className = 'error-message';
                    input.parentNode.insertBefore(errorMessage, input.nextElementSibling);
                }
                
                errorMessage.textContent = 'Please enter a valid email address';
                input.classList.add('invalid');
                return false;
            }
        }
        
        // If validation passes, remove any error message
        const errorMessage = input.nextElementSibling;
        if (errorMessage && errorMessage.classList.contains('error-message')) {
            errorMessage.textContent = '';
        }
        
        input.classList.remove('invalid');
        return true;
    }
    
    // Update session duration in real-time if it exists
    const sessionDurationElement = document.querySelector('.info-content p:nth-child(2)');
    
    if (sessionDurationElement && sessionDurationElement.textContent.includes('Current session duration:')) {
        // Extract the login time
        const loginTimeElement = document.querySelector('.info-content p:first-child');
        if (loginTimeElement) {
            const loginTimeText = loginTimeElement.textContent;
            const loginTime = loginTimeText.replace('Login time: ', '');
            
            // Update the session duration every second
            setInterval(function() {
                const loginDateTime = new Date(loginTime);
                const currentDateTime = new Date();
                const duration = currentDateTime - loginDateTime;
                
                const hours = Math.floor(duration / (1000 * 60 * 60));
                const minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((duration % (1000 * 60)) / 1000);
                
                sessionDurationElement.textContent = `Current session duration: ${hours}h ${minutes}m ${seconds}s`;
            }, 1000);
        }
    }
    
    // Add smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});