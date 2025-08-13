"""Compute baseline KPIs from aggregated run data."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List


def _entropy(dist: Dict[str, float]) -> float:
    total = sum(dist.values())
    if total <= 0:
        return 0.0
    ent = 0.0
    for value in dist.values():
        if value <= 0:
            continue
        p = value / total
        ent -= p * math.log2(p)
    return ent


def compute_metrics(rows: Iterable[Dict[str, str]]) -> Dict[str, float]:
    runs = set()
    decisions = 0
    trait_totals: Counter[str] = Counter()
    policy_counts: Counter[str] = Counter()

    for row in rows:
        runs.add(row["run"])
        decisions += 1
        policy_counts[row["policy"]] += 1
        final = json.loads(row["final_normalized"])
        for trait, value in final.items():
            trait_totals[trait] += value

    metrics: Dict[str, float] = {
        "runs": float(len(runs)),
        "decisions": float(decisions),
        "entropy": _entropy(trait_totals),
    }
    for policy, count in policy_counts.items():
        metrics[f"policy_{policy}_share"] = count / decisions if decisions else 0.0
    return metrics


def generate_report(metrics: Dict[str, float], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for key, value in sorted(metrics.items()):
            f.write(f"{key}: {value}\n")


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Compute baseline metrics")
    parser.add_argument("--in", dest="csv_in", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)

    with args.csv_in.open() as f:
        rows = list(csv.DictReader(f))
    metrics = compute_metrics(rows)
    generate_report(metrics, args.report)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
