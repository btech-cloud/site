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

const contactSubject = document.querySelector("#contact-subject");
const contactTypeInputs = document.querySelectorAll('input[name="contact_type"]');
const contactMessageLabel = document.querySelector("#contact-message-label");

const syncContactType = () => {
  const selected = document.querySelector('input[name="contact_type"]:checked');
  const isParceria = selected?.value === "parceria";

  if (contactSubject) {
    contactSubject.value = isParceria
      ? "Parceria — site BTech"
      : "Consultoria — site BTech";
  }

  const contactLabelText = document.querySelector("[data-contact-label]");
  if (contactLabelText) {
    contactLabelText.textContent = isParceria
      ? "Como imagina a parceria?"
      : "O que você quer organizar?";
  }

  if (contactMessageLabel) {
    const textarea = contactMessageLabel.querySelector("textarea");
    if (textarea instanceof HTMLTextAreaElement) {
      textarea.placeholder = isParceria
        ? "Ex.: MSP, integrador, vendor, co-entrega cloud, referência comercial..."
        : "Ex.: cloud, OpenShift, SAS, backup, CI/CD, IA...";
    }
  }
};

contactTypeInputs.forEach((input) => {
  input.addEventListener("change", syncContactType);
});

document.querySelectorAll("[data-contact-focus='parceria']").forEach((trigger) => {
  trigger.addEventListener("click", () => {
    const parceriaInput = document.querySelector('input[name="contact_type"][value="parceria"]');
    if (parceriaInput instanceof HTMLInputElement) {
      parceriaInput.checked = true;
      syncContactType();
    }
  });
});

syncContactType();

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
      syncContactType();
    } catch {
      formNote.textContent = `Não foi possível enviar agora. Escreva diretamente para ${targetEmail}.`;
    } finally {
      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = false;
      }
    }
  });
}
