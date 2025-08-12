"""Minimal engine loop with save/load, HUD toggle, and telemetry."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

from modules.tagging import tag
from modules.save_system import load_game, save_game
from modules.telemetry import Telemetry
from modules.reveal import load_reveals, pick_reveal


def default_state() -> Dict[str, Any]:
    return {"player": {"name": "Adventurer", "traits": {}}, "scene": "intro"}


def show_hud(state: Dict[str, Any]) -> None:
    print("== HUD ==")
    print(f"Player: {state['player']['name']}")
    for trait, value in state["player"]["traits"].items():
        print(f"  {trait}: {value}")
    print("==========")


def main(argv: Any = None) -> int:
    parser = argparse.ArgumentParser(description="Janus minimal engine")
    parser.add_argument("--load", help="Load game state from file")
    parser.add_argument("--save", help="Save game state to file")
    parser.add_argument("--no-hud", action="store_true", help="Disable HUD display")
    parser.add_argument("--telemetry", help="Write telemetry events to file")
    args = parser.parse_args(argv)

    state = default_state()
    if args.load:
        state = load_game(args.load)

    telemetry = Telemetry(args.telemetry)

    if state["player"]["name"] == "Adventurer":
        state["player"]["name"] = input("Enter your name: ") or "Adventurer"

    if not args.no_hud:
        show_hud(state)

    choice = {"id": "door", "text": "Open the ancient door"}
    choice = tag(choice, "Hubris", 0.5, "Fear", 0.2)
    print("1.", choice["text"])
    print("2. Walk away")
    selection = input("Choose 1 or 2: ").strip()
    if selection == "1":
        for tag_info in choice["tags"]:
            trait = tag_info["trait"]
            state["player"]["traits"][trait] = state["player"]["traits"].get(trait, 0.0) + tag_info["weight"]
        telemetry.log({"event": "choice", "id": "door", "selection": "open", "tags": choice["tags"]})
    else:
        telemetry.log({"event": "choice", "id": "door", "selection": "walk_away"})
    state["scene"] = "end"

    if args.save:
        save_game(state, args.save)
    telemetry.save()
    if not args.no_hud:
        show_hud(state)

    reveals_path = Path(__file__).resolve().parent.parent / "data" / "payoffs" / "endgame_reveals.json"
    reveal_data = load_reveals(reveals_path)
    reveal = pick_reveal(state["player"]["traits"], reveal_data)
    print("\n== Final Reflection ==")
    print(reveal["text"])
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main())
