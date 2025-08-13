"""Canonical trait mapping and validators."""

from __future__ import annotations

from typing import Dict

# Mapping of known duplicate trait labels to their canonical form
CANONICAL_MAP: Dict[str, str] = {
    "Control & Perfectionism": "Control",
    "Apathy & Sloth": "Apathy",
    "Pessimism & Cynicism": "Cynicism",
    "Cynicism": "Cynicism",
    "Moodiness & Indirectness": "Moodiness",
    "Fear & Insecurity": "Fear",
}

# Set of canonical trait names
CANONICAL_TRAITS = set(CANONICAL_MAP.values()) | {
    "Hubris",
    "Avarice",
    "Deception",
    "Wrath",
    "Impulsivity",
    "Rigidity",
    "Moodiness",
    "Control",
    "Fear",
    "Apathy",
    "Envy",
}


def canonicalize(trait: str) -> str:
    """Return canonical form of ``trait``.

    Raises
    ------
    ValueError
        If the trait is unknown and not already canonical.
    """

    if trait in CANONICAL_MAP:
        return CANONICAL_MAP[trait]
    if trait in CANONICAL_TRAITS:
        return trait
    raise ValueError(f"Unknown trait: {trait}")


def normalize_traits(mapping: Dict[str, float]) -> Dict[str, float]:
    """Normalize a trait->value mapping to canonical names.

    Duplicate entries are merged under the canonical label.
    """

    result: Dict[str, float] = {}
    for trait, value in mapping.items():
        canon = canonicalize(trait)
        result[canon] = result.get(canon, 0.0) + value
    return result


__all__ = ["canonicalize", "normalize_traits", "CANONICAL_MAP", "CANONICAL_TRAITS"]
