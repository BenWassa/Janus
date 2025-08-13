from __future__ import annotations

"""Persistent state manager tracking flags and trait scores."""
from typing import Any, Dict


class StateManager:
    """Centralized storage and retrieval for game state."""

    def __init__(self, state: Dict[str, Any]):
        self.state = state
        memory = state.setdefault("memory", {})
        self.state_flags: Dict[str, Any] = memory.setdefault("state_flags", {})
        self.trait_scores: Dict[str, float] = memory.setdefault("trait_scores", {})

    # ----- Flag management -------------------------------------------------
    def set_flag(self, name: str, value: Any = True) -> None:
        """Set ``name`` to ``value`` in the state flag dictionary."""
        self.state_flags[name] = value

    def get_flag(self, name: str, default: Any = None) -> Any:
        """Retrieve flag ``name`` or return ``default`` if unset."""
        return self.state_flags.get(name, default)

    def check_flag(self, name: str, value: Any = True) -> bool:
        """Return ``True`` if flag ``name`` equals ``value``."""
        return self.get_flag(name) == value

    # ----- Trait score management -----------------------------------------
    def add_trait(self, trait: str, weight: float) -> None:
        """Accumulate ``weight`` for ``trait`` in trait scores."""
        if weight > 0:
            self.trait_scores[trait] = self.trait_scores.get(trait, 0.0) + weight
