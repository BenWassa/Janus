from __future__ import annotations

"""Central symbol descriptions and trait mappings."""
from typing import Dict, Tuple

# Mapping of symbols to their associated traits (dominant vs alternative)
SYMBOL_TRAIT_MAP: Dict[str, Tuple[str, str]] = {
    "mirror": ("self_reflection", "avoidance"),
    "beast": ("aggression", "restraint"),
    "storm": ("unresolved_conflict", "decisiveness"),
}

# Text variations keyed by symbol and dominant trait.
SYMBOL_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    "mirror": {
        "self_reflection": "The mirror invites a hard look within.",
        "avoidance": "The mirror's surface clouds as you shy from it.",
    },
    "beast": {
        "aggression": "The beast's snarl deepens, daring confrontation.",
        "restraint": "The beast watches you, muscles tight but held in check.",
    },
    "storm": {
        "unresolved_conflict": "The storm churns with unresolved tensions.",
        "decisiveness": "The storm parts, revealing a brief path forward.",
    },
}


def describe(symbol: str, traits: Dict[str, float]) -> str:
    """Return a symbol description based on dominant related trait scores."""
    trait_pair = SYMBOL_TRAIT_MAP.get(symbol)
    if not trait_pair:
        return ""
    primary, secondary = trait_pair
    primary_score = traits.get(primary, 0.0)
    secondary_score = traits.get(secondary, 0.0)
    key = primary if primary_score >= secondary_score else secondary
    return SYMBOL_DESCRIPTIONS.get(symbol, {}).get(key, "")
