"""Utility for running simulations and writing detailed JSON artifacts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from testing.runner import run
from testing.policies import POLICIES


def write_run(
    policy_name: str,
    seed: int,
    max_steps: int = 100,
    dominance_threshold: int = 80,
    output_dir: Path | None = None,
) -> Dict[str, Any]:
    """Execute a run and write the detail JSON file.

    Parameters
    ----------
    policy_name:
        Name of the policy to execute.
    seed:
        Seed for deterministic execution.
    max_steps:
        Maximum number of steps to execute.
    dominance_threshold:
        Threshold used for trait dominance classification.
    output_dir:
        Base directory for results. Defaults to repository root.
    """

    policy_cls = POLICIES[policy_name]
    policy = policy_cls()
    result = run(policy, seed, max_steps)
    trace = result["trace"]
    final = result["final"]

    run_id = f"{policy_name}_{seed}"
    steps = len([t for t in trace if not t.get("end")])
    timeline = [
        {"step": t["step"], "totals": t["totals"]}
        for t in trace
        if not t.get("end")
    ]
    decisions = [
        {
            "step": t["step"],
            "sceneId": t.get("scene_id"),
            "choiceId": t.get("choice_id"),
            "text": t.get("text", ""),
            "primary": t.get("primary"),
            "pw": t.get("pw", 0.0),
            "secondary": t.get("secondary"),
            "sw": t.get("sw", 0.0),
        }
        for t in trace
        if not t.get("end")
    ]

    run_data: Dict[str, Any] = {
        "runId": run_id,
        "policy": policy_name,
        "seed": seed,
        "steps": steps,
        "normalized": final.get("normalized", {}),
        "top3": final.get("top3", []),
        "endingId": final.get("ending_id"),
        "flags": [],
        "timeline": timeline,
        "decisions": decisions,
        "revealText": final.get("revealText", ""),
        "timestamp": datetime.utcnow().isoformat(),
        "dominance_threshold": dominance_threshold,
    }

    out_dir = output_dir or Path(__file__).resolve().parents[2] / "data" / "test_results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"run_{run_id}.json"
    with out_file.open("w", encoding="utf-8") as fh:
        json.dump(run_data, fh, indent=2)

    return run_data


__all__ = ["write_run"]

