"""Assertion helpers for validating simulation traces."""

from __future__ import annotations

from typing import Dict, List, Iterable

from .runner import SCENE_WEIGHT_CAP, TRAIT_CAP_PER_ACT


def check_scene_caps(trace: Iterable[Dict]) -> List[str]:
    """Ensure per-scene weight cap is not exceeded."""

    errors: List[str] = []
    for step in trace:
        if step.get("end"):
            continue
        if sum(step.get("delta", {}).values()) > SCENE_WEIGHT_CAP:
            errors.append(f"scene_cap_exceeded:{step['scene_id']}")
    return errors


def check_trait_caps(trace: Iterable[Dict]) -> List[str]:
    """Validate that trait totals do not exceed the soft cap."""

    errors: List[str] = []
    for step in trace:
        if step.get("end"):
            continue
        for trait, total in step.get("totals", {}).items():
            if total > TRAIT_CAP_PER_ACT * 1.2:
                errors.append(f"trait_cap_exceeded:{trait}")
    return errors


def check_major_spacing(trace: Iterable[Dict]) -> List[str]:
    """Verify majors (+0.8) are not taken back to back."""

    errors: List[str] = []
    prev_major = False
    for step in trace:
        if step.get("end"):
            continue
        tags = step.get("delta", {})
        is_major = any(weight >= 0.8 for weight in tags.values())
        if is_major and prev_major:
            errors.append(f"major_spacing:{step['scene_id']}")
        prev_major = is_major
    return errors


def check_tag_integrity(trace: Iterable[Dict]) -> List[str]:
    """Ensure all chosen options contain required metadata."""

    errors: List[str] = []
    for step in trace:
        if step.get("end"):
            continue
        tags = step.get("delta", {})
        if not tags:
            errors.append(f"missing_tags:{step['scene_id']}")
    return errors


def assert_reveal_contains(trace: List[Dict], trait: str) -> None:
    """Raise if the final reveal does not include ``trait`` in the top-3."""

    final = trace[-1]
    top3 = final.get("top3", [])
    if trait not in top3:
        raise AssertionError(f"Expected {trait} in top3 but found {top3}")


__all__ = [
    "check_scene_caps",
    "check_trait_caps",
    "check_major_spacing",
    "check_tag_integrity",
    "assert_reveal_contains",
]

