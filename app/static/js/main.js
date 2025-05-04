// Form submit işlemi
document.addEventListener('DOMContentLoaded', function() {
    const urlForm = document.getElementById('urlForm');
    if (urlForm) {
        urlForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const urlInput = document.getElementById('urlInput');
            const resultDiv = document.getElementById('result');
            const shortUrlInput = document.getElementById('shortUrl');
            
            // Validate URL
            if (!isValidURL(urlInput.value)) {
                showAlert('Lütfen http:// veya https:// içeren geçerli bir URL girin', 'danger');
                return;
            }
            
            // Show loading indicator
            const submitBtn = e.target.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> İşleniyor...';
            submitBtn.disabled = true;
            
            try {
                const response = await fetch('/shorten', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `url=${encodeURIComponent(urlInput.value)}`
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    shortUrlInput.value = data.short_url;
                    resultDiv.classList.remove('d-none');
                    
                    // Scroll to result with smooth animation
                    resultDiv.scrollIntoView({ behavior: 'smooth' });
                    
                    // Flash effect
                    resultDiv.classList.add('highlight-animation');
                    setTimeout(() => resultDiv.classList.remove('highlight-animation'), 1000);
                } else {
                    showAlert(data.error || 'Bir hata oluştu', 'danger');
                }
            } catch (error) {
                showAlert('İsteğiniz işlenirken bir hata oluştu', 'danger');
                console.error(error);
            } finally {
                // Restore button state
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }
});

function copyUrl() {
    const shortUrlInput = document.getElementById('shortUrl');
    
    // Use modern Clipboard API if available
    if (navigator.clipboard) {
        navigator.clipboard.writeText(shortUrlInput.value)
            .then(() => {
                showCopyToast('URL panoya kopyalandı!');
            })
            .catch(err => {
                console.error('Could not copy text: ', err);
                fallbackCopy(shortUrlInput);
            });
    } else {
        fallbackCopy(shortUrlInput);
    }
}

// Fallback copy method for older browsers
function fallbackCopy(element) {
    element.select();
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopyToast('URL panoya kopyalandı!');
        } else {
            showAlert('URL kopyalanamadı', 'warning');
        }
    } catch (err) {
        console.error('Could not copy text: ', err);
        showAlert('URL kopyalanamadı', 'warning');
    }
}

// Show a toast notification
function showCopyToast(message) {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-check-circle me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Initialize and show the toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Show an alert message
function showAlert(message, type = 'info') {
    const alertsContainer = document.createElement('div');
    alertsContainer.className = 'alerts-container position-fixed top-0 start-50 translate-middle-x p-3';
    alertsContainer.style.zIndex = 1050;
    document.body.appendChild(alertsContainer);
    
    const alertId = 'alert-' + Date.now();
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    alertsContainer.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            const bsAlert = new bootstrap.Alert(alertElement);
            bsAlert.close();
        }
    }, 5000);
}

// Validate URL format
function isValidURL(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
} 