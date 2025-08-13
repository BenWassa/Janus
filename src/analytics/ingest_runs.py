"""Load and normalize run data into a canonical CSV."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List

from .canonical import canonicalize, normalize_traits

COLUMNS = [
    "run",
    "policy",
    "step",
    "scene_id",
    "choice_id",
    "primary",
    "secondary",
    "pw",
    "sw",
    "delta",
    "totals",
    "final_normalized",
    "top3",
]


def _rows_from_run(path: Path) -> Iterable[Dict[str, object]]:
    with path.open() as f:
        data = json.load(f)

    policy = data.get("policy", "")
    steps: List[Dict] = data.get("trait_progression", [])
    if not steps:
        return []

    # Final normalized traits and reveal are stored separately
    final_step = steps[-1]
    if final_step.get("end"):
        steps = steps[:-1]
    final_normalized = normalize_traits(final_step.get("normalized", {}))
    top3 = [canonicalize(t) for t in data.get("final_reveal", [])]

    rows: List[Dict[str, object]] = []
    for step in steps:
        row = {
            "run": step.get("run_id", path.stem),
            "policy": policy,
            "step": step.get("step"),
            "scene_id": step.get("scene_id"),
            "choice_id": step.get("choice_id"),
            "primary": canonicalize(step.get("primary")) if step.get("primary") else "",
            "secondary": canonicalize(step.get("secondary")) if step.get("secondary") else "",
            "pw": step.get("pw"),
            "sw": step.get("sw"),
            "delta": json.dumps(normalize_traits(step.get("delta", {})), sort_keys=True),
            "totals": json.dumps(normalize_traits(step.get("totals", {})), sort_keys=True),
            "final_normalized": json.dumps(final_normalized, sort_keys=True),
            "top3": json.dumps(top3),
        }
        rows.append(row)
    return rows


def ingest_runs(runs_dir: Path, out: Path) -> List[Dict[str, object]]:
    """Ingest run JSON files from ``runs_dir`` and write a CSV to ``out``."""

    all_rows: List[Dict[str, object]] = []
    for path in sorted(runs_dir.glob("run_*.json")):
        all_rows.extend(_rows_from_run(path))

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)
    return all_rows


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Ingest run data into a CSV")
    parser.add_argument("--runs-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    ingest_runs(args.runs_dir, args.out)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
