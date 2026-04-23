// Main JavaScript file for BHUMIPUTRA Platform

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 BHUMIPUTRA JavaScript initialized');
    console.log('🌐 Current URL:', window.location.href);
    console.log('📱 User Agent:', navigator.userAgent);
    console.log('🔧 Bootstrap available:', typeof bootstrap !== 'undefined');
    
    // Initialize tooltips only if bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        try {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
            console.log('✅ Tooltips initialized successfully');
        } catch (error) {
            console.error('❌ Tooltip initialization failed:', error);
        }
    } else {
        console.warn('⚠️ Bootstrap not available - tooltips disabled');
    }

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        console.log('📢 Found alerts to auto-hide:', alerts.length);
        
        alerts.forEach(function(alert, index) {
            try {
                if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                    console.log(`✅ Bootstrap alert ${index + 1} closed`);
                } else {
                    // Fallback: manually remove alert
                    alert.style.transition = 'opacity 0.5s';
                    alert.style.opacity = '0';
                    setTimeout(() => {
                        alert.remove();
                        console.log(`✅ Manual alert ${index + 1} removed`);
                    }, 500);
                }
            } catch (error) {
                console.error(`❌ Alert ${index + 1} closing failed:`, error);
            }
        });
    }, 5000);

    // Add smooth scrolling to all links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    console.log('🔗 Found anchor links:', anchorLinks.length);
    
    anchorLinks.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            console.log('🔗 Anchor link clicked:', this.getAttribute('href'));
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                console.log('🎯 Scrolling to target:', target);
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            } else {
                console.warn('⚠️ Target not found for anchor:', this.getAttribute('href'));
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    console.log('📋 Found validation forms:', forms.length);
    
    Array.prototype.slice.call(forms).forEach(function (form, index) {
        console.log(`📝 Setting up validation for form ${index + 1}:`, form.action || 'No action');
        
        form.addEventListener('submit', function (event) {
            console.log('🚀 Form submit event triggered');
            console.log('✅ Form validity on submit:', form.checkValidity());
            
            if (!form.checkValidity()) {
                console.log('❌ Preventing form submission due to validation errors');
                event.preventDefault();
                event.stopPropagation();
                
                // Log specific validation errors
                const invalidFields = form.querySelectorAll(':invalid');
                console.log(`❌ Found ${invalidFields.length} invalid fields:`);
                invalidFields.forEach((field, i) => {
                    console.error(`  ${i + 1}. ${field.name || field.id || 'unnamed'}: ${field.validationMessage}`);
                });
            } else {
                console.log('✅ Form is valid, allowing submission');
            }
            
            form.classList.add('was-validated');
        }, false);
    });

    // Loading spinner for form submissions
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    console.log('🔘 Found submit buttons:', submitButtons.length);
    
    submitButtons.forEach(function(button, index) {
        console.log(`🔘 Setting up button ${index + 1}:`, button.textContent.trim());
        
        button.addEventListener('click', function(e) {
            console.log('🔵 Submit button clicked:', button.textContent.trim());
            console.log('🔘 Button ID:', button.id || 'No ID');
            console.log('🔘 Button classes:', button.className);
            
            const form = button.closest('form');
            console.log('📝 Form found:', !!form);
            
            if (form) {
                console.log('� Form action:', form.action || 'No action');
                console.log('📝 Form method:', form.method || 'GET');
                console.log('📋 Form data entries:');
                
                // Log all form fields
                const formData = new FormData(form);
                for (let [key, value] of formData.entries()) {
                    console.log(`📄 ${key}:`, value);
                }
                
                console.log('✅ Form validity:', form.checkValidity());
                
                // Don't show loading state if form validation fails
                if (!form.checkValidity()) {
                    console.log('❌ Form validation failed - not submitting');
                    // Show validation errors
                    const invalidFields = form.querySelectorAll(':invalid');
                    console.log(`❌ Found ${invalidFields.length} invalid fields:`);
                    invalidFields.forEach((field, i) => {
                        console.error(`  ${i + 1}. ${field.name || field.id || 'unnamed'}: ${field.validationMessage}`);
                        console.error(`     Value: "${field.value}"`);
                        console.error(`     Type: ${field.type}`);
                        console.error(`     Required: ${field.required}`);
                    });
                    return;
                }
            } else {
                console.warn('⚠️ No form found for submit button');
            }
            
            console.log('⏳ Starting form submission process...');
            const originalText = button.innerHTML;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            button.disabled = true;
            
            // Re-enable after 5 seconds (in case of errors)
            setTimeout(function() {
                if (button) {
                    console.log('🔄 Resetting button state after timeout');
                    button.innerHTML = originalText;
                    button.disabled = false;
                }
            }, 5000);
        });
    });

    // Dynamic content loading simulation
    const loadMoreButtons = document.querySelectorAll('.load-more');
    loadMoreButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const originalText = button.innerHTML;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            button.disabled = true;
            
            // Simulate loading delay
            setTimeout(function() {
                button.innerHTML = originalText;
                button.disabled = false;
                // Add your content loading logic here
            }, 1500);
        });
    });

    // Search functionality
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(function(input) {
        input.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const searchTarget = this.getAttribute('data-search-target');
            
            if (searchTarget) {
                const items = document.querySelectorAll(searchTarget);
                items.forEach(function(item) {
                    const text = item.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        item.style.display = '';
                    } else {
                        item.style.display = 'none';
                    }
                });
            }
        });
    });

    // Cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name') || 'Product';
            
            // Add to cart logic here
            try {
                updateCartCount();
                showNotification(`${productName} added to cart!`);
            } catch (error) {
                console.warn('Cart functionality error:', error);
            }
        });
    });

    // Update cart count
    function updateCartCount() {
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            // Get current count and increment
            let count = parseInt(cartCount.textContent) || 0;
            cartCount.textContent = count + 1;
        }
    }

    // Show notification
    function showNotification(message) {
        try {
            const notification = document.createElement('div');
            notification.className = 'alert alert-success alert-dismissible fade show position-fixed';
            notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
            notification.innerHTML = `
                ${message}
                <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
            `;
            
            document.body.appendChild(notification);
            
            // Auto-remove after 3 seconds
            setTimeout(function() {
                if (notification && notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 3000);
        } catch (error) {
            console.warn('Notification error:', error);
            // Fallback: use console.log
            console.log('Notification:', message);
        }
    }

    // Image preview for file uploads
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.querySelector('#image-preview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const password = this.value;
            const strengthIndicator = document.querySelector('#password-strength');
            
            if (strengthIndicator) {
                const strength = calculatePasswordStrength(password);
                strengthIndicator.className = `password-strength ${strength.level}`;
                strengthIndicator.textContent = strength.message;
            }
        });
    });

    // Calculate password strength
    function calculatePasswordStrength(password) {
        let strength = 0;
        
        if (password.length >= 8) strength++;
        if (password.match(/[a-z]/)) strength++;
        if (password.match(/[A-Z]/)) strength++;
        if (password.match(/[0-9]/)) strength++;
        if (password.match(/[^a-zA-Z0-9]/)) strength++;
        
        const levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
        const classes = ['danger', 'warning', 'info', 'primary', 'success'];
        
        return {
            level: classes[strength] || 'danger',
            message: levels[strength] || 'Very Weak'
        };
    }

    // Dashboard statistics animation
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(function(stat) {
        const target = parseInt(stat.getAttribute('data-target'));
        if (!isNaN(target) && target > 0) {
            const duration = 2000; // 2 seconds
            const increment = target / (duration / 16); // 60fps
            let current = 0;
            
            const timer = setInterval(function() {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                stat.textContent = Math.floor(current);
            }, 16);
        }
    });

    // Print functionality
    const printButtons = document.querySelectorAll('.print-btn');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Export to CSV functionality
    const exportButtons = document.querySelectorAll('.export-csv');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const tableId = this.getAttribute('data-table');
            exportTableToCSV(tableId);
        });
    });

    // Export table to CSV
    function exportTableToCSV(tableId) {
        try {
            const table = document.querySelector(tableId);
            if (!table) {
                console.warn('Table not found:', tableId);
                return;
            }
            
            let csv = [];
            const rows = table.querySelectorAll('tr');
            
            rows.forEach(function(row) {
                const cols = row.querySelectorAll('td, th');
                const rowData = Array.from(cols).map(function(col) {
                    return col.textContent.trim();
                });
                csv.push(rowData.join(','));
            });
            
            const csvContent = csv.join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'export.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.warn('CSV export error:', error);
        }
    }
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-IN');
}

function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?');
}

// AJAX helper function
function makeAjaxRequest(url, method, data, callback) {
    try {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        callback(response);
                    } catch (parseError) {
                        console.warn('JSON parse error:', parseError);
                        callback(xhr.responseText);
                    }
                } else {
                    console.warn('Request failed:', xhr.statusText);
                }
            }
        };
        
        xhr.send(JSON.stringify(data));
    } catch (error) {
        console.error('AJAX request error:', error);
    }
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
