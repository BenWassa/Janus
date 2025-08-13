"""Trait scoring and archetype utilities."""
from __future__ import annotations

from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Archetype mappings
# ---------------------------------------------------------------------------

# Single-trait archetypes retained for backward compatibility and as a
# fallback when no meaningful pair is detected.
ARCHETYPES: Dict[str, Tuple[str, str]] = {
    "Hubris": ("The Ascendant", "soaring ever higher beyond all limits."),
    "Avarice": ("The Collector", "gathering all that glitters into your grasp."),
    "Deception": ("The Maskbearer", "hiding truths behind careful facades."),
    "Control": ("The Architect", "shaping every path to your design."),
    "Wrath": ("The Flame", "letting fury blaze at every turn."),
    "Fear": ("The Shade", "moving with caution in the looming dark."),
}

# New dual-trait archetype mapping for Sprint 22.  Keys are alphabetical
# tuples of the top two traits.
COMBO_ARCHETYPES: Dict[Tuple[str, str], Tuple[str, str]] = {
    ("aggression", "decisiveness"): (
        "The Challenger",
        "You face obstacles head-on and demand immediate resolution.",
    ),
    ("aggression", "avoidance"): (
        "The Rebel",
        "You push against every restraint yet shrink from reflection.",
    ),
    ("decisiveness", "restraint"): (
        "The Strategist",
        "You weigh options carefully and strike with precision.",
    ),
    ("restraint", "self_reflection"): (
        "The Harmonizer",
        "You resist chaos, seeking balance over dominance.",
    ),
    ("self_reflection", "unresolved_conflict"): (
        "The Brooder",
        "You dwell on inner turmoil in search of meaning.",
    ),
}

DEFAULT_ARCHETYPE = ("The Enigma", "leaving little of yourself revealed.")

def normalize_scores(traits: Dict[str, float]) -> Dict[str, float]:
    """Return traits normalized to percentages of the total weight."""
    total = sum(traits.values())
    if total <= 0:
        return {}
    return {trait: value / total for trait, value in traits.items()}

def top_archetype(traits: Dict[str, float]) -> Tuple[str, str]:
    """Return an archetype based on the dominant one or two traits.

    The two highest-weighted traits are considered.  If their combination
    appears in ``COMBO_ARCHETYPES`` an associated archetype is returned.
    Otherwise the single highest trait is mapped via ``ARCHETYPES``.  If
    neither mapping yields a result, ``DEFAULT_ARCHETYPE`` is used.
    """

    if not traits:
        return DEFAULT_ARCHETYPE

    # Sort traits by descending weight
    ordered = sorted(traits.items(), key=lambda i: i[1], reverse=True)
    top_trait = ordered[0][0]
    second_trait = ordered[1][0] if len(ordered) > 1 else None

    if second_trait:
        key = tuple(sorted((top_trait, second_trait)))
        if key in COMBO_ARCHETYPES:
            return COMBO_ARCHETYPES[key]

    return ARCHETYPES.get(top_trait, DEFAULT_ARCHETYPE)
