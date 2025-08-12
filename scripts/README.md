# Scripts Directory

Convenient launcher scripts for Project Janus.

## Files

### `run_alpha.bat`
Launch the alpha build in **user mode** (recommended for players and testers).
- Clean, immersive experience
- No trait debugging information visible
- Saves telemetry to `outputs/user_session.json`

### `run_alpha_debug.bat`
Launch the alpha build in **developer mode** (for development and analysis).
- Full trait visibility and debugging info
- Shows choice effects and psychological weights
- Saves telemetry to `outputs/debug_session.json`

## Usage

Double-click the appropriate `.bat` file, or run from command line:

```bash
# User mode
scripts\run_alpha.bat

# Developer mode  
scripts\run_alpha_debug.bat
```

## Prerequisites

- Alpha build must be created first: `python deployment/build_alpha.py`
- Alpha build should be extracted to `dist/janus_v2-alpha/`
