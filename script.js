// Lucide icons
if (window.lucide) lucide.createIcons();

// Mobile navigation toggle
const navToggle = document.querySelector('.nav__toggle');
const nav = document.querySelector('.nav');

if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', open);
  });
  nav.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Story category filter (clanky.html)
const filterBar = document.querySelector('.filter-bar');
if (filterBar) {
  filterBar.addEventListener('click', (e) => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    filterBar.querySelectorAll('.chip').forEach(c => c.classList.remove('is-active'));
    chip.classList.add('is-active');
    const cat = chip.dataset.cat;
    document.querySelectorAll('.story-card').forEach(card => {
      card.style.display = (cat === 'all' || card.dataset.cat === cat) ? '' : 'none';
    });
  });
}

// Fade-in on scroll
const fadeEls = document.querySelectorAll('.fade-in');
if ('IntersectionObserver' in window && fadeEls.length) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  fadeEls.forEach(el => io.observe(el));
} else {
  fadeEls.forEach(el => el.classList.add('visible'));
}
