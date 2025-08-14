# Prototype Humility Hubris

This module hosts the prototype demonstrating the Humility–Hubris continuum for Project Janus.

## Quickstart

1. Navigate to `frontend/`.
2. Open `index.html` in a modern browser or serve the directory with `python -m http.server`.
3. Explore the choices and watch trait feedback in real time.

## Structure

- `frontend/index.html` – experimental web interface with dynamic trait visuals, constellation canvas, and decision mechanics.
- `docs/html_upgrade_sprints.md` – sprint plan outlining progressive enhancements for the HTML prototype.
- Python modules (`continuum.py`, `payoff_hook.py`, `registrar.py`, `symbol_variants.py`) implement backend logic for the continuum experiments.

The prototype now separates styling and logic into dedicated `style.css`, `data.js`, and `app.js` files. Future iterations will expand multi-trait support as detailed in the sprint plan.
