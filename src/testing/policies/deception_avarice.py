"""Deception + Avarice archetype policy."""

from __future__ import annotations

from typing import Dict

from .base import RuleBasedPolicy


class DeceptionAvaricePolicy(RuleBasedPolicy):
    """Seeks profit and advantage through cunning.

    Choices that advance ``Deception`` or ``Avarice`` are rewarded heavily.
    Altruistic or selfless options (``Apathy & Sloth`` here as a stand-in for
    self-denial) are discouraged.
    """

    def __init__(self) -> None:
        prefer: Dict[str, float] = {
            "Deception": 2.0,
            "Avarice": 2.0,
        }
        avoid: Dict[str, float] = {
            "Apathy & Sloth": 1.0,
        }
        super().__init__(prefer, avoid)


__all__ = ["DeceptionAvaricePolicy"]

