const menuButton = document.querySelector(".nav__toggle");
const menu = document.querySelector(".nav__links");
const currentYear = document.querySelector("#current-year");
const contactForm = document.querySelector(".contact__form");
const formNote = document.querySelector(".form-note");

if (currentYear) {
  currentYear.textContent = new Date().getFullYear();
}

if (menuButton && menu) {
  menuButton.addEventListener("click", () => {
    const isExpanded = menuButton.getAttribute("aria-expanded") === "true";

    menuButton.setAttribute("aria-expanded", String(!isExpanded));
    menu.classList.toggle("is-open", !isExpanded);
  });

  menu.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      menuButton.setAttribute("aria-expanded", "false");
      menu.classList.remove("is-open");
    }
  });
}

if (contactForm && formNote) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    formNote.textContent = "Mensagem pronta para envio. Configure um servico de formulario para receber contatos.";
    contactForm.reset();
  });
}
