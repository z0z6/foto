// ========== LIGHTBOX ==========

function openLightbox(src, caption) {
    const lightbox = document.getElementById('lightbox');
    const img = document.getElementById('lightbox-img');
    const cap = document.getElementById('lightbox-caption');

    img.src = src;
    cap.textContent = caption || '';
    lightbox.classList.add('active');

    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('active');

    document.body.style.overflow = '';
}

// Zamknij lightbox klawiszem ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLightbox();
    }
});

// Pokaż zdjęcia stopniowo przy scrollowaniu
document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.gallery-item');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    items.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = `opacity 0.6s ease ${index * 0.03}s, transform 0.6s ease ${index * 0.03}s`;
        observer.observe(item);
    });
});
