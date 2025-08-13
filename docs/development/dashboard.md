# Testing Dashboard & Calibration Monitor

An interactive dashboard for running Janus simulation policies, visualising trait progression, and experimenting with calibration settings.

## Setup

The dashboard relies on Dash and Plotly. Dependencies are installed automatically on first launch, but you can pre-install them:

```bash
pip install dash plotly
```

## Running

Start the dashboard from the repository root:

```bash
python src/dashboard/run_dashboard.py
```

### Features

- Choose between built-in policies and run simulations with a click
- Tabbed charts for trait progression, final scores, and decision trees
- Quick stats summarising recent runs
- Dedicated "Calibration" tab with a mixer interface for policy multipliers
- Each run is saved under `data/test_results/` for later inspection

### Calibration Monitor

Open the **Calibration** tab to access the experimental "Personality Mixer." Use the sliders to adjust policy multipliers and master controls such as decay, anti-streak, and epsilon. Readouts update in real time while providing a foundation for future calibration tooling.
