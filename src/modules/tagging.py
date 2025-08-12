"""Choice processing and trait tagging utilities."""
from __future__ import annotations
from typing import Dict, List, Optional

TRAITS = {
    "Hubris",
    "Avarice",
    "Deception",
    "Control",
    "Wrath",
    "Fear",
    "Impulsivity",
    "Envy",
    "Apathy",
    "Cynicism",
    "Moodiness",
    "Rigidity",
}


def tag(choice: Dict[str, any],
        primary_trait: str,
        primary_weight: float,
        secondary_trait: Optional[str] = None,
        secondary_weight: float = 0.0) -> Dict[str, any]:
    """Attach trait tags to a choice.

    Parameters
    ----------
    choice: dict
        Data structure for the choice (id, text, etc.).
    primary_trait: str
        Main trait to weight.
    primary_weight: float
        Weight applied to the primary trait.
    secondary_trait: str | None
        Optional secondary trait.
    secondary_weight: float
        Weight for the secondary trait.

    Returns
    -------
    dict
        Updated choice with a ``tags`` list in the canonical format.
    """
    if primary_trait not in TRAITS:
        raise ValueError("Unknown primary trait")
    tags: List[Dict[str, float]] = [{"trait": primary_trait, "weight": primary_weight}]
    if secondary_trait:
        if secondary_trait not in TRAITS:
            raise ValueError("Unknown secondary trait")
        tags.append({"trait": secondary_trait, "weight": secondary_weight})
    choice["tags"] = tags
    return choice


def normalize(trait_totals: Dict[str, float],
              scene_cap: float = 0.8,
              act_cap: float = 2.0) -> Dict[str, float]:
    """Normalize trait totals to meet design caps.

    - Combined weight per scene is limited to ``scene_cap``.
    - Each trait is soft-capped at ``act_cap`` per act.
    """
    scene_total = sum(trait_totals.values())
    if scene_total > scene_cap:
        factor = scene_cap / scene_total
        for trait in trait_totals:
            trait_totals[trait] *= factor
    for trait in trait_totals:
        if trait_totals[trait] > act_cap:
            trait_totals[trait] = act_cap
    return trait_totals

