"""Control + Fear archetype policy."""

from __future__ import annotations

from typing import Dict

from .base import RuleBasedPolicy


class ControlFearPolicy(RuleBasedPolicy):
    """Cautious, planning-oriented decision maker.

    The policy promotes restraint and methodical choices by favouring
    ``Control & Perfectionism`` and ``Fear & Insecurity`` tags.  It actively
    avoids reckless traits such as ``Impulsivity`` or destructive ``Wrath``
    options.
    """

    def __init__(self) -> None:
        prefer: Dict[str, float] = {
            "Control & Perfectionism": 2.0,
            "Fear & Insecurity": 1.5,
        }
        avoid: Dict[str, float] = {
            "Impulsivity": 2.0,
            "Wrath": 1.0,
        }
        super().__init__(prefer, avoid)


__all__ = ["ControlFearPolicy"]

