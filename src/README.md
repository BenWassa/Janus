# Source Code

Core engine entry point and reusable modules.

## Components
- **engine.py** – Minimal game loop with CLI options for save/load, HUD toggle, telemetry logging, and endgame trait reveal.
- **modules/** – Reusable engine modules (`tagging.py`, `save_system.py`, `telemetry.py`, `reveal.py`).

## Engine CLI

```
python src/engine.py [--load FILE] [--save FILE] [--no-hud] [--telemetry FILE]
```
- `--load` loads a previously saved state.
- `--save` writes the current state in JSON format.
- `--no-hud` suppresses the HUD display.
- `--telemetry` records gameplay events to a JSON file.

## Design Principles
- Modular and extensible architecture
- Clean separation of concerns
- Easy integration with psychology profiling
- Support for multiple game versions
