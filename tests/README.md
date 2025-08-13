# Testing Suite

Automated tests verify engine behavior, scoring algorithms, telemetry logging, and calibration utilities.

## Structure
- `test_canonical.py` – ensures narrative flows match golden records.
- `test_calibrator_bounds.py` – validates calibrator parameter bounds.
- `test_ingest_schema.py` – checks input schema consistency.
- `test_optimizer_objective.py` – verifies optimization objective calculations.
- `test_reveal.py` – tests trait-based reveal messages.
- `test_run_output.py` – confirms engine run outputs.
- `test_scoring.py` – validates trait scoring logic.
- `test_telemetry.py` – verifies telemetry capture and storage.

Supporting directories:
- `goldens/` – expected outputs for canonical tests.
- `config/` – configuration files for test runs.
- `reports/` – latest test suite reports.

## Running Tests
```bash
python -m pytest
```
