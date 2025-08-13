# Testing Dashboard

An interactive dashboard for running Janus simulation policies and visualising trait progression.

## Setup

Install the required packages:

```bash
pip install dash plotly
```

## Running

Start the dashboard from the repository root:

```bash
python src/dashboard/run_dashboard.py
```

A browser window will open with controls to select a policy and execute a run.  Results are saved under `data/test_results/` for later inspection.
