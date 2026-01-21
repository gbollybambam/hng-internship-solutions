document.addEventListener('DOMContentLoaded', () => {

    // --- 1. UTC Time Display ---
    function updateTime() {
        const timeElement = document.querySelector('[data-testid="test-user-time"]');
        if (timeElement) {
            timeElement.textContent = Date.now();
        }
    }
    updateTime();
    setInterval(updateTime, 1000);

    // --- 2. 3D Interactive Card Effect ---
    const card = document.querySelector('.profile-card');
    if (card) {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -4;
            const rotateY = ((x - centerX) / centerX) * 4;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
        });
    }
    
    // --- 3. Staggered Animation on Load ---
    const timeline = [];
    const mainCard = document.querySelector('.profile-card');
    if (mainCard) timeline.push({ el: mainCard, delay: 0 });

    const elementsToAnimate = [
        'figure', 'h2', 'p',
        'ul[data-testid="test-user-social-links"]', '.user-details', '.about-section', '.contact-header', '#contact-form'
    ];
    elementsToAnimate.forEach((selector, index) => {
        document.querySelectorAll(selector).forEach(item => {
            timeline.push({ el: item, delay: 200 + index * 100 });
        });
    });

    timeline.forEach(item => {
        setTimeout(() => {
            item.el.style.opacity = '1';
            item.el.style.transform = 'translateY(0)';
            item.el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        }, item.delay);
    });

    // --- 4. Contact Form Validation ---
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        const successMessage = document.querySelector('[data-testid="test-contact-success"]');
        
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            let isValid = true;

            document.querySelectorAll('.error-message').forEach(el => {
                el.textContent = '';
                el.style.display = 'none';
            });

            const name = document.querySelector('[data-testid="test-contact-name"]');
            const email = document.querySelector('[data-testid="test-contact-email"]');
            const subject = document.querySelector('[data-testid="test-contact-subject"]');
            const message = document.querySelector('[data-testid="test-contact-message"]');

            if (name.value.trim() === '') {
                showError(name, 'Full name is required.');
                isValid = false;
            }
            if (!isValidEmail(email.value)) {
                showError(email, 'Please enter a valid email address.');
                isValid = false;
            }
            if (subject.value.trim() === '') {
                showError(subject, 'Subject is required.');
                isValid = false;
            }
            if (message.value.trim().length < 10) {
                showError(message, 'Message must be at least 10 characters long.');
                isValid = false;
            }

            if (isValid) {
                successMessage.textContent = 'Thank you! Your message has been sent successfully.';
                successMessage.style.display = 'block';
                contactForm.style.display = 'none';
            }
        });

        function showError(inputElement, message) {
            const errorElement = document.querySelector(`[data-testid="test-contact-error-${inputElement.id}"]`);
            if (errorElement) {
                errorElement.textContent = message;
                errorElement.style.display = 'block';
                inputElement.setAttribute('aria-describedby', errorElement.id);
            }
        }

        function isValidEmail(email) {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return regex.test(email);
        }
    }
});