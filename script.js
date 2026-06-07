const header = document.querySelector("[data-header]");

if (header) {
  const syncHeader = () => {
    header.classList.toggle("site-header--elevated", window.scrollY > 16);
  };

  syncHeader();
  window.addEventListener("scroll", syncHeader, { passive: true });
}

const menuButton = document.querySelector(".nav__toggle");
const menu = document.querySelector(".nav__links");
const currentYear = document.querySelector("#current-year");
const contactForm = document.querySelector(".contact-form");
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
  const endpoint = contactForm.dataset.formEndpoint?.trim() || "";
  const targetEmail = contactForm.dataset.formEmail?.trim() || "comercial@b-tech.cloud";

  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!endpoint) {
      formNote.textContent =
        "Envio não configurado. Escreva para comercial@b-tech.cloud ou ligue (11) 9 3022-6495.";
      return;
    }

    const submitButton = contactForm.querySelector('button[type="submit"]');
    const formData = new FormData(contactForm);
    const payload = Object.fromEntries(formData.entries());

    if (submitButton instanceof HTMLButtonElement) {
      submitButton.disabled = true;
    }

    formNote.textContent = "Enviando…";

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Falha no envio");
      }

      formNote.textContent = `Mensagem enviada. Em breve retornamos no e-mail informado (destino: ${targetEmail}).`;
      contactForm.reset();
    } catch {
      formNote.textContent = `Não foi possível enviar agora. Escreva diretamente para ${targetEmail}.`;
    } finally {
      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = false;
      }
    }
  });
}
