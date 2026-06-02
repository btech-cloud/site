# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **static institutional website** (HTML, CSS, vanilla JavaScript). There is no package manager, build step, backend, or Docker.

### Running the site locally

From the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` (home) and `http://localhost:8000/cloud.html` (cloud offering page).

Prefer serving over HTTP rather than opening `index.html` via `file://`, so relative assets and browser behavior match production-like usage.

### Lint / test / build

There are **no** configured linters, unit tests, or build commands in this repo. Validation is manual or smoke-based:

- `curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/` (and `/cloud.html`, `/styles.css`, `/styles-vivid.css`, `/styles-mockup.css`, `/script.js`, `/assets/logo-btech-horizontal-oficial.png`) should return `200`.
- In the browser: mobile nav toggle (`.nav__toggle`), footer year (`#current-year`), and contact form submit (shows the Portuguese note in `.form-note`; no network request).

### Services

| Service | Notes |
|--------|--------|
| Static HTTP server | **Required** for dev/E2E — e.g. `python3 -m http.server 8000` |

### Logo assets

Official lockups are raster exports from `assets/source/logo-btech-canva.pdf`. Regenerate with:

```bash
python3 scripts/build-logos.py
```

(requires `pdftoppm` from poppler-utils)
| Browser | **Required** for UI checks |

No environment variables or secrets are used.

### Gotchas

- The contact form is **client-only** (`preventDefault` in `script.js`); submitting does not send email or call an API.
- If port 8000 is busy, any port works; update the URL accordingly.

See `README.md` for product context and file layout.
