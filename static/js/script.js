// Theme toggle (dark/light)
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Check saved preference or system preference
    if (localStorage.getItem('theme') === 'light' || 
        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: light)').matches)) {
        html.setAttribute('data-bs-theme', 'light');
        toggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
    }

    toggle.addEventListener('click', () => {
        if (html.getAttribute('data-bs-theme') === 'dark') {
            html.setAttribute('data-bs-theme', 'light');
            toggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
            localStorage.setItem('theme', 'light');
        } else {
            html.setAttribute('data-bs-theme', 'dark');
            toggle.innerHTML = '<i class="bi bi-moon-stars-fill"></i>';
            localStorage.setItem('theme', 'dark');
        }
    });
});