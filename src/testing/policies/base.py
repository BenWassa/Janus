"""Utility helpers for scripted policies."""

from __future__ import annotations

from typing import Dict, List
import random


class RuleBasedPolicy:
    """Base class implementing simple trait based scoring.

    Subclasses define ``prefer`` and ``avoid`` dictionaries mapping trait
    names to weight multipliers.  During decision making each option is scored
    by multiplying the option's trait weights with these multipliers.
    """

    prefer: Dict[str, float]
    avoid: Dict[str, float]

    def __init__(self, prefer: Dict[str, float], avoid: Dict[str, float] | None = None):
        self.prefer = prefer
        self.avoid = avoid or {}

    # ------------------------------------------------------------------
    def score_option(self, option: Dict[str, any]) -> float:
        """Compute a preference score for a single option."""

        score = 0.0
        tags = option["tags"]
        for trait_key, weight_key in ("primary", "pw"), ("secondary", "sw"):
            trait = tags.get(trait_key)
            weight = tags.get(weight_key, 0.0)
            if trait in self.prefer:
                score += weight * self.prefer[trait]
            if trait in self.avoid:
                score -= weight * self.avoid[trait]
        return score

    # ------------------------------------------------------------------
    def __call__(self, state: Dict, rng: random.Random) -> str:
        """Return the ``choice_id`` for the best scoring option."""

        best_score: float | None = None
        best_options: List[Dict] = []
        for opt in state["options"]:
            score = self.score_option(opt)
            if best_score is None or score > best_score:
                best_score = score
                best_options = [opt]
            elif score == best_score:
                best_options.append(opt)

        chosen = rng.choice(best_options)
        return chosen["choice_id"]


__all__ = ["RuleBasedPolicy"]

