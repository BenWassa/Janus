#!/usr/bin/env python3
"""Validate and preview scene JSON files for pilot_humility_hubris.

This script loads all `.json` files from `pilot_humility_hubris/scenes/`,
checks that they conform to `docs/scene-schema.md`, and optionally
runs a deterministic preview of a single playthrough.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCENES_DIR = Path(__file__).resolve().parent.parent / "pilot_humility_hubris" / "scenes"

REQUIRED_SCENE_FIELDS = {"id", "title", "text", "options"}
REQUIRED_OPTION_FIELDS = {"id", "label", "delta"}


def load_scenes() -> Tuple[Dict[str, dict], str]:
    """Return scenes keyed by id and the default starting scene id."""
    index_path = SCENES_DIR / "index.json"
    with index_path.open() as f:
        order = json.load(f)["scenes"]
    scenes: Dict[str, dict] = {}
    start_id: Optional[str] = None
    for name in order:
        path = SCENES_DIR / name
        with path.open() as f:
            data = json.load(f)
        scenes[data["id"]] = data
        if start_id is None:
            start_id = data["id"]
    if start_id is None:
        raise ValueError("No scenes found")
    return scenes, start_id


def validate_scene(scene: dict) -> None:
    missing = REQUIRED_SCENE_FIELDS - scene.keys()
    if missing:
        raise ValueError(f"Scene {scene.get('id')} missing fields: {missing}")
    if not isinstance(scene["options"], list) or not scene["options"]:
        raise ValueError(f"Scene {scene['id']} must contain options")
    for opt in scene["options"]:
        missing_opt = REQUIRED_OPTION_FIELDS - opt.keys()
        if missing_opt:
            raise ValueError(
                f"Option {opt.get('id')} in scene {scene['id']} missing fields: {missing_opt}"
            )
        if not isinstance(opt["delta"], dict):
            raise ValueError(
                f"Option {opt['id']} in scene {scene['id']} has non-dict delta"
            )


def validate_all(scenes: Dict[str, dict]) -> None:
    for scene in scenes.values():
        validate_scene(scene)
    print(f"Validated {len(scenes)} scene(s).")


def preview(
    scenes: Dict[str, dict],
    seed: Optional[int] = None,
    start: Optional[str] = None,
    path: Optional[List[str]] = None,
) -> List[str]:
    rng = random.Random(seed)
    current = start or next(iter(scenes))
    taken: List[str] = []
    while current:
        scene = scenes[current]
        options = scene["options"]
        if path:
            choice_id = path.pop(0)
            choice = next((o for o in options if o["id"] == choice_id), None)
            if choice is None:
                raise ValueError(f"Choice {choice_id} not found in scene {current}")
        else:
            choice = rng.choice(options)
        taken.append(choice["id"])
        current = choice.get("next")
    return taken


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and preview scenes")
    parser.add_argument("--preview", action="store_true", help="run a preview after validation")
    parser.add_argument("--seed", type=int, default=None, help="random seed for preview")
    parser.add_argument("--start", help="starting scene id")
    parser.add_argument("--path", nargs="*", help="explicit option id path for replay")
    args = parser.parse_args()

    scenes, default_start = load_scenes()
    validate_all(scenes)
    if args.preview:
        path = list(args.path) if args.path else None
        start = args.start or default_start
        taken = preview(scenes, seed=args.seed, start=start, path=path)
        print("Preview path:", " -> ".join(taken))
        if args.seed is not None:
            print("Replay code:", json.dumps({"seed": args.seed, "path": taken}))


if __name__ == "__main__":
    main()
