"""Hubris-forward archetype policy."""

from __future__ import annotations

from typing import Dict

from .base import RuleBasedPolicy


class HubrisForwardPolicy(RuleBasedPolicy):
    """Prefer bold, dominant options associated with Hubris.

    This policy strongly favours choices tagged with ``Hubris`` and mildly
    favours ``Control & Perfectionism``.  Options evoking fear or retreat
    (``Fear & Insecurity``) are penalised.  When multiple options share the
    same score the policy uses the supplied RNG to select among them.
    """

    def __init__(self) -> None:
        prefer: Dict[str, float] = {
            "Hubris": 2.0,
            "Control & Perfectionism": 1.0,
        }
        avoid: Dict[str, float] = {
            "Fear & Insecurity": 1.0,
        }
        super().__init__(prefer, avoid)


__all__ = ["HubrisForwardPolicy"]

