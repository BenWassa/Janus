"""Seeded random policy used for Monte-Carlo style exploration."""

from __future__ import annotations

from typing import Dict, List, Set
import random


class SeededRandomPolicy:
    """Deterministic random decision policy.

    The policy prefers options that have not been seen before in a given run
    and avoids selecting more than two major (0.8 weight) choices in a row.
    """

    def __init__(self) -> None:
        self.seen: Set[str] = set()
        self.major_streak: int = 0

    # ------------------------------------------------------------------
    def __call__(self, state: Dict, rng: random.Random) -> str:
        options: List[Dict] = state["options"]

        # Avoid picking majors three times consecutively
        candidates = options
        if self.major_streak >= 2:
            non_major = [
                o for o in options if o["tags"].get("pw", 0.0) < 0.8 and o["tags"].get("sw", 0.0) < 0.8
            ]
            if non_major:
                candidates = non_major

        # Prefer unseen options for broader coverage
        unseen = [o for o in candidates if o["choice_id"] not in self.seen]
        choice = rng.choice(unseen or candidates)

        tags = choice["tags"]
        if tags.get("pw", 0.0) >= 0.8 or tags.get("sw", 0.0) >= 0.8:
            self.major_streak += 1
        else:
            self.major_streak = 0

        self.seen.add(choice["choice_id"])
        return choice["choice_id"]


__all__ = ["SeededRandomPolicy"]

