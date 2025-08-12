"""Simple JSON-based save/load utilities."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def save_game(state: Dict[str, Any], path: str) -> None:
    """Save ``state`` to ``path`` as JSON.

    Parameters
    ----------
    state: dict
        Arbitrary serialisable game state.
    path: str
        Destination file path.
    """
    with open(Path(path), "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def load_game(path: str) -> Dict[str, Any]:
    """Load game state from ``path``.

    Parameters
    ----------
    path: str
        Source JSON file path.

    Returns
    -------
    dict
        Parsed game state.
    """
    with open(Path(path), "r", encoding="utf-8") as f:
        return json.load(f)
