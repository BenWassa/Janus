"""Balanced human archetype policy."""

from __future__ import annotations

from typing import Dict, List
import random


class BalancedHumanPolicy:
    """Pick moderate options and occasionally decoys.

    This policy does not rely on a simple trait preference.  Instead it looks
    for options whose weight sits in the mid range (0.2–0.5) and avoids
    extremes.  With a small probability it will select a decoy option to
    mimic human inconsistency.
    """

    def __init__(self, decoy_chance: float = 0.1) -> None:
        self.decoy_chance = decoy_chance

    # ------------------------------------------------------------------
    def __call__(self, state: Dict, rng: random.Random) -> str:
        options: List[Dict] = state["options"]

        decoys = [o for o in options if o.get("is_decoy")]
        if decoys and rng.random() < self.decoy_chance:
            return rng.choice(decoys)["choice_id"]

        def weight_distance(opt: Dict) -> float:
            tags = opt["tags"]
            pw = tags.get("pw", 0.0)
            return abs(0.35 - pw)  # prefer mid weights around 0.35

        options = sorted(options, key=weight_distance)
        top_score = weight_distance(options[0])
        best = [o for o in options if weight_distance(o) == top_score]
        return rng.choice(best)["choice_id"]


__all__ = ["BalancedHumanPolicy"]

