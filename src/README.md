# Source Code

Core engine entry point and reusable modules.

## Components
- **engine.py** – Minimal game loop with save/load, HUD toggle, telemetry logging, and endgame trait reveal. The HUD displays current trait totals and details of the last choice.
- **modules/** – Reusable engine modules (`tagging.py`, `save_system.py`, `telemetry.py`, `reveal.py`).
- **cli/** – Command-line helpers and entry points.
- **dashboard/** – Dash-powered interface for running simulation policies, visualising trait progression, and experimenting with calibration.
- **calibrator/** – Tools for applying policy multipliers and optimizing configuration snapshots.
- **testing/** – Harness utilities, policies, and metrics for automated runs.

## Engine CLI

```
python src/engine.py [--load FILE] [--save FILE] [--no-hud] [--telemetry FILE]
```
- `--load` loads a previously saved state.
- `--save` writes the current state in JSON format.
- `--no-hud` suppresses the HUD display.
- `--telemetry` records choice events (ID and trait weights) to a JSON file.

## Design Principles
- Modular and extensible architecture
- Clean separation of concerns
- Easy integration with psychology profiling
- Support for multiple game versions
