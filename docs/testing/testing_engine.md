# Testing Engine

This directory documents the alpha testing engine used to simulate player
decision paths.  The tool can execute scripted policies or deterministic
random runs against the current story content.

## Usage

Run a single policy:

```bash
python -m src.cli.testrig run --policy hubris --seed 1 --runs 1
```

Run a suite over all policies:

```bash
python -m src.cli.testrig suite --all --seed 1 --runs 1
```

Outputs are written to `tests/artifacts` as JSON Lines files.  A Markdown
summary of the last suite run is stored in `tests/reports/last_suite.md`.

