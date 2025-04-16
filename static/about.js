document.addEventListener('DOMContentLoaded', function() {
    const carouselContainer = document.querySelector('.carousel-container');
    const carouselSlides = document.querySelectorAll('.carousel-slide');
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');
    const indicatorsContainer = document.querySelector('.carousel-indicators');

    let currentIndex = 0;
    const slideCount = carouselSlides.length;
    let autoSlideInterval;

    // Function to update the carousel display
    function updateCarousel() {
        carouselContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
        updateIndicators();
        // Animate slide transition
        carouselSlides.forEach((slide, index) => {
            slide.style.opacity = index === currentIndex ? '1' : '0';
            slide.style.transform = index === currentIndex ? 'scale(1)' : 'scale(0.95)';
        });
    }

    // Function to create and update indicators
    function updateIndicators() {
        indicatorsContainer.innerHTML = '';
        for (let i = 0; i < slideCount; i++) {
            const indicator = document.createElement('div');
            indicator.classList.add('indicator');
            indicator.addEventListener('click', () => {
                currentIndex = i;
                updateCarousel();
                resetAutoSlide();
            });
            if (i === currentIndex) {
                indicator.classList.add('active');
            }
            indicatorsContainer.appendChild(indicator);
        }
    }

    // Auto-slide functionality
    function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
            currentIndex = (currentIndex + 1) % slideCount;
            updateCarousel();
        }, 5000);
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    // Event listeners for navigation buttons
    prevButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + slideCount) % slideCount;
        updateCarousel();
        resetAutoSlide();
    });

    nextButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % slideCount;
        updateCarousel();
        resetAutoSlide();
    });

    // Pause auto-slide on hover
    carouselContainer.addEventListener('mouseenter', () => {
        clearInterval(autoSlideInterval);
    });

    carouselContainer.addEventListener('mouseleave', () => {
        startAutoSlide();
    });

    // Initialize carousel and indicators
    updateCarousel();
    startAutoSlide();

    // Animate elements on scroll
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    animateElements.forEach(el => observer.observe(el));
});