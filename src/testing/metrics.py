"""Metrics helpers for simulation suites."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Set


def path_coverage(traces: Iterable[List[Dict]]) -> Set[str]:
    """Return set of unique scene identifiers visited."""

    scenes: Set[str] = set()
    for trace in traces:
        for step in trace:
            if step.get("end"):
                continue
            scenes.add(step["scene_id"])
    return scenes


def choice_coverage(traces: Iterable[List[Dict]]) -> Set[str]:
    """Return set of unique choice identifiers exercised."""

    choices: Set[str] = set()
    for trace in traces:
        for step in trace:
            if step.get("end"):
                continue
            choices.add(step["choice_id"])
    return choices


def trait_distribution(traces: Iterable[List[Dict]]) -> Dict[str, float]:
    """Compute mean trait totals across runs."""

    totals: Dict[str, float] = defaultdict(float)
    runs = 0
    for trace in traces:
        runs += 1
        final = trace[-1]
        for trait, value in final.get("normalized", {}).items():
            totals[trait] += value

    if runs == 0:
        return {}
    return {trait: value / runs for trait, value in totals.items()}


def reveal_accuracy_rate(finals: Iterable[Dict], trait: str) -> float:
    """Return fraction of runs where ``trait`` appears in top3."""

    finals = list(finals)
    if not finals:
        return 0.0
    hits = sum(1 for f in finals if trait in f.get("top3", []))
    return hits / len(finals)


__all__ = [
    "path_coverage",
    "choice_coverage",
    "trait_distribution",
    "reveal_accuracy_rate",
]

