"""Parameter optimizer for calibration configs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple


class Optimizer:
    """Evaluate candidate configurations with a composite objective."""

    @staticmethod
    def score(balance: float, deviation: float, intent_lock: bool = True) -> float:
        """Higher balance and lower deviation improve the score.

        Lack of intent lock applies a heavy penalty.
        """
        score = balance - deviation
        if not intent_lock:
            score -= 1.0
        return score

    def optimize(self, candidates: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """Return the best configuration and its statistics."""
        best_cfg: Dict[str, Any] | None = None
        best_stats: Dict[str, float] | None = None
        best_score = float("-inf")

        for stats in candidates.values():
            score = self.score(
                stats.get("balance", 0.0),
                stats.get("policy_deviation", 0.0),
                stats.get("intent_lock", True),
            )
            if score > best_score:
                best_score = score
                best_cfg = stats.get("config", {})
                best_stats = stats

        return best_cfg or {}, best_stats or {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        base_config = json.load(f)

    # In lieu of a full search, use the baseline as the sole candidate.
    candidates = {
        "baseline": {
            "config": base_config,
            "balance": 0.0,
            "policy_deviation": 0.0,
            "intent_lock": True,
        }
    }

    optimizer = Optimizer()
    best_config, stats = optimizer.optimize(candidates)

    result = {
        "config": best_config,
        "stats": stats,
        "hash": hashlib.sha256(json.dumps(best_config, sort_keys=True).encode()).hexdigest(),
    }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":  # pragma: no cover
    main()
