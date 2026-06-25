/** BTech Cloud — carrossel, animações, painéis de serviço */

(function () {
  const header = document.querySelector("[data-header]");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Hero carousel */
  const hero = document.querySelector("[data-hero]");
  if (hero) {
    const slides = [...hero.querySelectorAll(".hero__slide")];
    const dots = [...hero.querySelectorAll("[data-hero-dot]")];
    const prev = hero.querySelector("[data-hero-prev]");
    const next = hero.querySelector("[data-hero-next]");
    let index = 0;
    let timer;

    const go = (i) => {
      index = (i + slides.length) % slides.length;
      slides.forEach((s, n) => s.classList.toggle("is-active", n === index));
      dots.forEach((d, n) => {
        d.classList.toggle("is-active", n === index);
        d.setAttribute("aria-selected", n === index ? "true" : "false");
      });
    };

    const start = () => {
      clearInterval(timer);
      timer = setInterval(() => go(index + 1), 7000);
    };

    prev?.addEventListener("click", () => { go(index - 1); start(); });
    next?.addEventListener("click", () => { go(index + 1); start(); });
    dots.forEach((d) => {
      d.addEventListener("click", () => {
        go(Number(d.dataset.heroDot));
        start();
      });
    });

    hero.addEventListener("mouseenter", () => clearInterval(timer));
    hero.addEventListener("mouseleave", start);
    start();
  }

  /* Reveal on scroll */
  const revealEls = document.querySelectorAll(".reveal, [data-step]");
  if (revealEls.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* Service panels — Saiba mais */
  const panelsWrap = document.getElementById("service-panels");
  const toggles = document.querySelectorAll("[data-service-toggle]");
  if (panelsWrap && toggles.length) {
    panelsWrap.hidden = false;
    toggles.forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const id = link.dataset.serviceToggle;
        const panel = document.getElementById(`panel-${id}`);
        if (!panel) return;
        const open = panel.classList.contains("is-open");
        panelsWrap.querySelectorAll(".service-detail").forEach((p) => p.classList.remove("is-open"));
        if (!open) {
          panel.classList.add("is-open");
          panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      });
    });
  }
})();
