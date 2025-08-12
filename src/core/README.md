# Core Game Engine

This module contains the fundamental components that power the Janus RPG system.

## Components

- **engine.py** – Minimal game loop with CLI options for save/load, HUD toggle, and telemetry logging.
- **save_system.py** – JSON-based game state persistence.
- **telemetry.py** – Lightweight gameplay event logger.

## Engine CLI

```
python src/core/engine.py [--load FILE] [--save FILE] [--no-hud] [--telemetry FILE]
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
