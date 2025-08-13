from __future__ import annotations

"""Persistent state flag manager."""
from typing import Any, Dict


class StateManager:
    """Centralized storage and retrieval for game state flags."""

    def __init__(self, state: Dict[str, Any]):
        self.state = state
        self.state.setdefault("flags", {})

    def set_flag(self, name: str, value: Any = True) -> None:
        """Set ``name`` to ``value`` in the flag dictionary."""
        self.state["flags"][name] = value

    def get_flag(self, name: str, default: Any = None) -> Any:
        """Retrieve flag ``name`` or return ``default`` if unset."""
        return self.state["flags"].get(name, default)

    def check_flag(self, name: str, value: Any = True) -> bool:
        """Return ``True`` if ``name`` equals ``value``."""
        return self.get_flag(name) == value
