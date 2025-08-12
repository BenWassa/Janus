"""Core simulation runner for the alpha testing engine.

This module exposes a :func:`run` function that executes scripted play
policies against the current scenario content.  It performs minimal rule
enforcement (scene caps, trait caps, major spacing) and returns a complete
trace suitable for further analysis.

The implementation here is intentionally lightweight – it does not attempt
to emulate the full game engine.  It simply iterates through the scenario
data files and feeds metadata to a policy object which decides which choice
to take next.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Any, Tuple


# ---------------------------------------------------------------------------
# Constants

# Trait names referenced in content.  They are used only for book keeping and
# do not represent an exhaustive list of psychological features.
TRAITS: List[str] = [
    "Hubris",
    "Avarice",
    "Deception",
    "Control & Perfectionism",
    "Wrath",
    "Fear & Insecurity",
    "Impulsivity",
    "Envy",
    "Apathy & Sloth",
    "Pessimism & Cynicism",
    "Moodiness & Indirectness",
    "Rigidity",
]

# Rule constants – deliberately kept simple so that the harness can operate in
# isolation from the main game engine.
SCENE_WEIGHT_CAP = 0.8
TRAIT_CAP_PER_ACT = 2.0


# ---------------------------------------------------------------------------
# Helpers

def _data_path() -> Path:
    """Return the repository data directory."""

    return Path(__file__).resolve().parents[2] / "data" / "scenarios"


def load_scenarios() -> List[Dict[str, Any]]:
    """Load all scenes across acts.

    Each returned element is a dictionary describing a single scene with an
    additional ``act`` field.
    """

    mapping = {
        1: "act1_mirrors.json",
        2: "act2_beasts.json",
        3: "act3_whispers.json",
    }

    scenes: List[Dict[str, Any]] = []
    for act, fname in mapping.items():
        file = _data_path() / fname
        if not file.exists():
            continue
        with file.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            for scene in data.get("scenes", []):
                scene = dict(scene)
                scene["act"] = act
                scenes.append(scene)
    return scenes


# ---------------------------------------------------------------------------
# Runner

StateSnapshot = Dict[str, Any]
Policy = Callable[[StateSnapshot, random.Random], str]


def run(play_policy: Policy, seed: int, max_steps: int = 100) -> Dict[str, Any]:
    """Execute a simulation run.

    Parameters
    ----------
    play_policy:
        Callable that selects a ``choice_id``.  It receives the current state
        snapshot and a :class:`random.Random` instance for deterministic
        behaviour.
    seed:
        Seed used to initialise the RNG.
    max_steps:
        Maximum number of steps to execute.

    Returns
    -------
    dict
        Mapping containing the full trace under ``"trace"`` and the final
        summary under ``"final"``.
    """

    rng = random.Random(seed)
    scenarios = load_scenarios()

    totals: Dict[str, float] = {t: 0.0 for t in TRAITS}
    act_step: Dict[int, int] = {1: 0, 2: 0, 3: 0}
    trace: List[Dict[str, Any]] = []
    last_major_step = -99

    for idx, scene in enumerate(scenarios, start=1):
        if idx > max_steps:
            break

        act = scene["act"]
        act_step[act] += 1
        options: List[Dict[str, Any]] = []

        for choice in scene.get("choices", []):
            option = {
                "choice_id": choice.get("choice_id"),
                "scene_id": scene.get("scene_id"),
                "text": choice.get("text", ""),
                "tags": {
                    "primary": choice.get("primary_trait"),
                    "pw": float(choice.get("primary_weight", 0.0)),
                    "secondary": choice.get("secondary_trait"),
                    "sw": float(choice.get("secondary_weight", 0.0)),
                },
                "is_decoy": (
                    float(choice.get("primary_weight", 0.0)) == 0.0
                    and float(choice.get("secondary_weight", 0.0)) == 0.0
                ),
            }
            options.append(option)

        snapshot: StateSnapshot = {
            "act": act,
            "scene_id": scene.get("scene_id"),
            "options": options,
            "totals": totals.copy(),
            "step": idx - 1,
            "act_step": act_step[act] - 1,
        }

        choice_id = play_policy(snapshot, rng)
        chosen = next((o for o in options if o["choice_id"] == choice_id), options[0])
        tags = chosen["tags"]

        # Tag integrity checks
        if not tags.get("primary"):
            raise ValueError("Choice missing primary trait tag")
        if tags.get("secondary") and tags.get("sw", 0.0) > tags.get("pw", 0.0):
            raise ValueError("Secondary weight exceeds primary weight")

        delta: Dict[str, float] = {}
        if tags.get("primary") and tags.get("pw", 0.0) > 0:
            trait = tags["primary"]
            weight = tags["pw"]
            totals[trait] = totals.get(trait, 0.0) + weight
            delta[trait] = weight
        if tags.get("secondary") and tags.get("sw", 0.0) > 0:
            trait = tags["secondary"]
            weight = tags["sw"]
            totals[trait] = totals.get(trait, 0.0) + weight
            delta[trait] = weight

        flags: List[str] = []
        scene_total = sum(delta.values())
        if scene_total <= SCENE_WEIGHT_CAP:
            flags.append("scene_cap_ok")
        else:
            flags.append("scene_cap_fail")

        is_major = tags.get("pw", 0.0) >= 0.8 or tags.get("sw", 0.0) >= 0.8
        if is_major and idx - last_major_step <= 1:
            flags.append("major_spacing_fail")
        else:
            flags.append("major_spacing_ok")
            if is_major:
                last_major_step = idx

        for trait, value in totals.items():
            if value > TRAIT_CAP_PER_ACT * 1.2:
                flags.append("trait_cap_fail")
                break

        trace.append(
            {
                "run_id": f"run_{seed}",
                "step": idx,
                "scene_id": scene.get("scene_id"),
                "choice_id": chosen["choice_id"],
                "delta": delta,
                "totals": totals.copy(),
                "flags": flags,
                "end": False,
            }
        )

    total_points = sum(totals.values()) or 1.0
    normalized = {
        trait: int(value / total_points * 100)
        for trait, value in totals.items()
        if value > 0
    }
    top3 = sorted(normalized, key=normalized.get, reverse=True)[:3]

    final = {
        "run_id": f"run_{seed}",
        "end": True,
        "normalized": normalized,
        "top3": top3,
        "ending_id": None,
        "payoffs": {},
    }

    trace.append(final)
    return {"trace": trace, "final": final}


__all__ = ["run", "load_scenarios", "TRAITS"]

