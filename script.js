const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('.nav__toggle');
const menu = document.querySelector('.nav__links');
const currentYear = document.querySelector('#current-year');
const contactForm = document.querySelector('.contact-form');
const formNote = document.querySelector('.form-note');
const slides = Array.from(document.querySelectorAll('.hero__slide'));
const pager = document.querySelector('[data-hero-pager]');

if (header) {
  const syncHeader = () => header.classList.toggle('is-elevated', window.scrollY > 12);
  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });
}

if (currentYear) {
  currentYear.textContent = new Date().getFullYear();
}

if (menuButton && menu) {
  menuButton.addEventListener('click', () => {
    const isExpanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!isExpanded));
    menu.classList.toggle('is-open', !isExpanded);
  });

  menu.addEventListener('click', (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      menuButton.setAttribute('aria-expanded', 'false');
      menu.classList.remove('is-open');
    }
  });
}

if (slides.length && pager) {
  let activeIndex = 0;
  const buttons = slides.map((_, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.setAttribute('aria-label', `Mostrar slide ${index + 1}`);
    button.addEventListener('click', () => showSlide(index, true));
    pager.append(button);
    return button;
  });

  function showSlide(index, userAction = false) {
    activeIndex = index;
    slides.forEach((slide, slideIndex) => slide.classList.toggle('is-active', slideIndex === activeIndex));
    buttons.forEach((button, buttonIndex) => button.classList.toggle('is-active', buttonIndex === activeIndex));
    if (userAction) window.clearInterval(slideTimer);
  }

  showSlide(0);
  const slideTimer = window.setInterval(() => showSlide((activeIndex + 1) % slides.length), 6500);
}

if (contactForm && formNote) {
  contactForm.addEventListener('submit', (event) => {
    event.preventDefault();
    formNote.textContent = 'Obrigado. Recebemos sua intenção de contato; envie também para comercial@b-tech.cloud para seguirmos a conversa.';
    contactForm.reset();
  });
}
