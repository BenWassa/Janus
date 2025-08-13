"""Trait scoring and archetype utilities."""
from __future__ import annotations

from typing import Dict, Tuple

# Mapping of dominant traits to archetypal summaries.
ARCHETYPES: Dict[str, Tuple[str, str]] = {
    "Hubris": ("The Ascendant", "soaring ever higher beyond all limits."),
    "Avarice": ("The Collector", "gathering all that glitters into your grasp."),
    "Deception": ("The Maskbearer", "hiding truths behind careful facades."),
    "Control": ("The Architect", "shaping every path to your design."),
    "Wrath": ("The Flame", "letting fury blaze at every turn."),
    "Fear": ("The Shade", "moving with caution in the looming dark."),
}

DEFAULT_ARCHETYPE = ("The Enigma", "leaving little of yourself revealed.")

def normalize_scores(traits: Dict[str, float]) -> Dict[str, float]:
    """Return traits normalized to percentages of the total weight."""
    total = sum(traits.values())
    if total <= 0:
        return {}
    return {trait: value / total for trait, value in traits.items()}

def top_archetype(traits: Dict[str, float]) -> Tuple[str, str]:
    """Determine the archetype represented by the highest-weighted trait."""
    if not traits:
        return DEFAULT_ARCHETYPE
    top_trait = max(traits.items(), key=lambda i: i[1])[0]
    return ARCHETYPES.get(top_trait, DEFAULT_ARCHETYPE)
