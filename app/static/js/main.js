document.getElementById('urlForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const urlInput = document.getElementById('urlInput');
    const resultDiv = document.getElementById('result');
    const shortUrlInput = document.getElementById('shortUrl');
    
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
        } else {
            alert(data.error || 'Bir hata oluştu');
        }
    } catch (error) {
        alert('Bir hata oluştu');
    }
});

function copyUrl() {
    const shortUrlInput = document.getElementById('shortUrl');
    shortUrlInput.select();
    document.execCommand('copy');
    alert('URL kopyalandı!');
} 