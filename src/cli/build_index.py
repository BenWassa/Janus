"""Generate a summary index for run artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

SUMMARY_KEYS = [
    "runId",
    "policy",
    "seed",
    "steps",
    "normalized",
    "top3",
    "endingId",
    "flags",
    "timestamp",
    "dominance_threshold",
]


def build_index(results_dir: Path | None = None) -> List[Dict[str, Any]]:
    """Rebuild the run summary index.

    Parameters
    ----------
    results_dir:
        Directory containing ``run_*.json`` files. Defaults to ``data/test_results``
        under the repository root.
    """

    base = results_dir or Path(__file__).resolve().parents[2] / "data" / "test_results"
    runs: List[Dict[str, Any]] = []
    if not base.exists():
        return runs

    for file in sorted(base.glob("run_*.json")):
        with file.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        summary = {key: data.get(key) for key in SUMMARY_KEYS}
        runs.append(summary)

    index_file = base / "index.json"
    with index_file.open("w", encoding="utf-8") as fh:
        json.dump(runs, fh, indent=2)

    return runs


__all__ = ["build_index"]

