import csv
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from analytics.ingest_runs import COLUMNS, ingest_runs


def test_ingest_runs_schema(tmp_path):
    runs_dir = Path("data/test_results")
    out = tmp_path / "runs_agg.csv"
    rows = ingest_runs(runs_dir, out)

    # Ensure CSV has expected columns
    with out.open() as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == COLUMNS
        csv_rows = list(reader)

    # Row count should equal sum of decisions across runs
    total_decisions = 0
    for path in runs_dir.glob("run_*.json"):
        with path.open() as f:
            data = json.load(f)
        total_decisions += data.get("decisions_made", 0)
    assert len(csv_rows) == total_decisions
    assert len(rows) == total_decisions
