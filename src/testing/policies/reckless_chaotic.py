"""Reckless + Chaotic archetype policy."""

from __future__ import annotations

from typing import Dict

from .base import RuleBasedPolicy


class RecklessChaoticPolicy(RuleBasedPolicy):
    """Impulsive, high variance decision maker.

    Strongly favours ``Impulsivity`` and aggressive ``Wrath`` options, while
    steering away from calculated ``Control & Perfectionism`` traits.
    """

    def __init__(self) -> None:
        prefer: Dict[str, float] = {
            "Impulsivity": 2.0,
            "Wrath": 1.5,
        }
        avoid: Dict[str, float] = {
            "Control & Perfectionism": 2.0,
        }
        super().__init__(prefer, avoid)


__all__ = ["RecklessChaoticPolicy"]

