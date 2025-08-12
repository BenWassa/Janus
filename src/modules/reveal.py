"""Endgame trait reveal helpers."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def load_reveals(path: str | Path) -> Dict[str, Any]:
    """Load reveal definitions from ``path``.

    Parameters
    ----------
    path: str | Path
        Location of the ``endgame_reveals.json`` file.
    """
    with open(Path(path), "r", encoding="utf-8") as f:
        return json.load(f)


def top_traits(traits: Dict[str, float], count: int = 3) -> List[str]:
    """Return the top ``count`` traits sorted by weight."""
    return [t for t, _ in sorted(traits.items(), key=lambda i: i[1], reverse=True)[:count]]


def pick_reveal(traits: Dict[str, float], reveals: Dict[str, Any]) -> Dict[str, str]:
    """Select a reveal based on the player's top two traits.

    Parameters
    ----------
    traits: dict
        Mapping of trait names to accumulated weights.
    reveals: dict
        Reveal data loaded via :func:`load_reveals`.

    Returns
    -------
    dict
        Dictionary with ``id`` and ``text`` keys for the chosen reveal.
    """
    top = top_traits(traits, 2)
    if len(top) < 2 or traits[top[0]] == traits[top[1]]:
        fallback = reveals["neutral_fallback"]
        return {"id": fallback["id"], "text": fallback["template"]}

    primary, secondary = top
    for tpl in reveals["reveal_templates"]:
        if tpl["primary_trait"] == primary and tpl["secondary_trait"] == secondary:
            text = tpl["template"].format(
                primary_trait=primary,
                secondary_trait=secondary,
                primary_metaphor=reveals["trait_metaphors"][primary],
                secondary_metaphor=reveals["trait_metaphors"][secondary],
            )
            return {"id": tpl["id"], "text": text}

    fallback = reveals["neutral_fallback"]
    return {"id": fallback["id"], "text": fallback["template"]}
