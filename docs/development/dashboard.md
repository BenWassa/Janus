# Testing Dashboard

An interactive dashboard for running Janus simulation policies and visualising trait progression.

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
- View line charts of trait progression and bar charts of final scores
- Each run is saved under `data/test_results/` for later inspection
