# Prototype Humility Hubris

This module hosts the prototype demonstrating the Humility–Hubris continuum for Project Janus.

## Quickstart

1. Navigate to `frontend/`.
2. Open `index.html` in a modern browser or serve the directory with `python -m http.server`.
3. Explore the choices and watch trait feedback in real time.

## Structure


The prototype now separates styling and logic into dedicated `style.css`, `data.js`, and `app.js` files. Future iterations will expand multi-trait support as detailed in the sprint plan.
# Prototype Humility — Hubris (frontend)

This module contains a small interactive prototype demonstrating the Humility–Hubris continuum used in Project Janus.

## Quickstart

1. Open a terminal and change to the frontend folder:

	cd pilot_humility_hubris/frontend

2. Serve the folder or open the static `index.html` directly in a modern browser. To run a quick HTTP server (Python 3):

	python -m http.server 8000

	Then open http://localhost:8000 in your browser.

3. Interact with the UI: make decisions and watch the trait feedback and constellation visuals update in real time.

## Recent frontend upgrades

- Refactored UI into separate static assets: `index.html`, `style.css`, `data.js`, and `app.js`.
- Moved data/configuration out of the HTML into `data.js` for easier tuning and automated tests.
- Implemented an event-driven UI in `app.js` with improved responsiveness and smoother animations.
- Basic accessibility improvements: clearer focus states and semantic controls (see `index.html`).
- No build step or npm dependencies — the frontend is a static prototype and can be served from any static host.

## File overview

- `index.html` — entry point and markup for the experimental UI.
- `style.css` — styles and responsive layout rules.
- `data.js` — prototype data model and configuration used by the UI.
- `app.js` — UI behavior, event wiring, and visual updates.

## Development notes

- The frontend is intentionally lightweight and dependency-free. Use the browser console for debugging; `app.js` exposes simple init and state hooks.
- If you need to iterate faster, use a live-reload dev server. Two convenient options:

- VS Code Live Server extension: install the extension and click "Go Live" in the status bar to serve the `frontend/` folder and get live reload.
- Run via npx (no global install required) from PowerShell in the frontend folder:

```powershell
cd pilot_humility_hubris/frontend
npx live-server . --port=5500
```

Alternatively install globally with `npm install -g live-server` and run `live-server . --port=5500`.
- To propose changes, update the relevant file in `pilot_humility_hubris/frontend/` and open a PR describing the UI/userflow change.

## Related docs

- See `docs/html_upgrade_sprints.md` for the sprint plan and planned enhancements.
- Backend logic for experiments lives in the module files `continuum.py`, `payoff_hook.py`, `registrar.py`, and `symbol_variants.py`.

## Notes

This README focuses on the frontend prototype. For integration details or dataset formats, consult the root README or the `data/` directory.
