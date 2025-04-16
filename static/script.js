document.addEventListener('DOMContentLoaded', () => {

    // --- Navbar Scroll Effect ---
    const header = document.querySelector('.site-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // --- Mobile Navigation Toggle ---
    const navToggle = document.getElementById('nav-toggle');
    const mainNav = document.getElementById('main-nav');

    if (navToggle && mainNav) {
        navToggle.addEventListener('click', () => {
            document.body.classList.toggle('nav-open'); // Toggle class on body
            mainNav.classList.toggle('is-active'); // Toggle active class on nav itself
            const isExpanded = mainNav.classList.contains('is-active');
            navToggle.setAttribute('aria-expanded', isExpanded);
        });

        // Optional: Close nav when a link is clicked (useful for single-page apps or # links)
        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (document.body.classList.contains('nav-open')) {
                     document.body.classList.remove('nav-open');
                     mainNav.classList.remove('is-active');
                     navToggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    // --- Scroll Animation ---
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    if (animateElements.length > 0 && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // Optional: Stop observing once visible to save resources
                    // obs.unobserve(entry.target);
                } else {
                    // Optional: Remove 'visible' if you want animation to repeat when scrolling up
                    // entry.target.classList.remove('visible');
                }
            });
        }, {
            threshold: 0.15, // Trigger when 15% of the element is visible
            // rootMargin: "0px 0px -50px 0px" // Optional: Adjust trigger point
        });

        animateElements.forEach(el => observer.observe(el));
    } else {
        // Fallback for browsers without IntersectionObserver or if no elements found
        animateElements.forEach(el => el.classList.add('visible')); // Make them visible directly
    }


    // --- Smooth Scroll for internal Anchor Links ---
    // The check for 'a[href^="#"]' ensures we only target internal links
    // The check '&& link.getAttribute('href') !== '#'' prevents targeting empty hashes
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        if (anchor.getAttribute('href') !== '#') { // Avoid targeting href="#" links
             anchor.addEventListener('click', function (e) {
                const hrefAttribute = this.getAttribute('href');
                // Check if it's a valid ID selector
                if (hrefAttribute.length > 1 && hrefAttribute.startsWith('#')) {
                    const targetElement = document.querySelector(hrefAttribute);
                    if (targetElement) {
                        e.preventDefault(); // Prevent default jump only if target exists
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start' // Or 'center'
                        });
                    }
                }
            });
        }
    });

    // --- Dynamic Footer Year ---
    const yearSpan = document.getElementById('current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // --- Lazy Load Images (already in home.html, keep it there or consolidate) ---
    // If you want all images with a specific class lazy-loaded:
    // const lazyImages = document.querySelectorAll('img.lazy'); // Add class="lazy" to images
    // lazyImages.forEach(img => {
    //     img.setAttribute('loading', 'lazy');
    // });


    // --- FUTURE INTERACTIVITY EXAMPLE (using Fetch API) ---
    // Example: Check date availability dynamically (requires backend endpoint)
    /*
    const dateInput = document.getElementById('appointment-date-input'); // Assuming you have this input on the booking page
    if (dateInput) {
        dateInput.addEventListener('change', async (event) => {
            const selectedDate = event.target.value;
            const availabilityStatus = document.getElementById('availability-status'); // Element to display status

            if (!selectedDate || !availabilityStatus) return;

            availabilityStatus.textContent = 'Checking...';
            availabilityStatus.style.color = 'grey';

            try {
                // Replace '/check-availability' with your actual backend endpoint
                const response = await fetch(`/check-availability?date=${selectedDate}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json(); // Assuming backend returns { available: true/false }

                if (data.available) {
                    availabilityStatus.textContent = 'Date is available!';
                    availabilityStatus.style.color = 'green';
                } else {
                    availabilityStatus.textContent = 'Date is already booked.';
                    availabilityStatus.style.color = 'red';
                }
            } catch (error) {
                console.error('Error checking availability:', error);
                availabilityStatus.textContent = 'Could not check availability.';
                availabilityStatus.style.color = 'orange';
            }
        });
    }
    */

}); // End DOMContentLoaded