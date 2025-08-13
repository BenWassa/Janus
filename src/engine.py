"""
Enhanced v2-alpha engine that loads scenarios from JSON data files.
This replaces the minimal stub with a full game implementation.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

from modules.tagging import tag
from modules.save_system import load_game, save_game
from modules.telemetry import Telemetry
from modules.reveal import load_reveals, pick_reveal
from modules.state_manager import StateManager


def default_state() -> Dict[str, Any]:
    """Initial game state."""
    return {
        "player": {"name": "Adventurer", "traits": {}},
        "current_act": 1,
        "current_scene": 0,
        "completed_scenes": [],
        "last_choice": None,
        "flags": {},
    }


def show_hud(state: Dict[str, Any], debug_mode: bool = False) -> None:
    """Display game HUD with player status."""
    if debug_mode:
        print("== DEBUG HUD ==")
        print(f"Player: {state['player']['name']}")
        print(f"Act: {state['current_act']}")

        # Show traits if any exist (debug only)
        traits = state["player"]["traits"]
        if traits:
            for trait, value in sorted(traits.items()):
                print(f"  {trait}: {value:.1f}")

        # Show flags if any exist (debug only)
        flags = state.get("flags", {})
        if flags:
            print("Flags:")
            for flag, val in flags.items():
                print(f"  {flag}: {val}")
        
        # Show last choice info (debug only)
        last = state.get("last_choice")
        if last:
            print("Last Choice:")
            print(f"  ID: {last['id']}")
            if last.get("primary_trait"):
                print(f"  Primary: {last['primary_trait']} ({last['primary_weight']})")
            if last.get("secondary_trait"):
                print(f"  Secondary: {last['secondary_trait']} ({last['secondary_weight']})")
    else:
        print("== Status ==")
        print(f"Player: {state['player']['name']}")
        act_names = {1: "Mirrors", 2: "Beasts", 3: "Whispers"}
        print(f"Act: {state['current_act']} - {act_names.get(state['current_act'], 'Unknown')}")
        
        # Show only story-relevant info for users
        last = state.get("last_choice")
        if last and last.get("id") != "unknown":
            print(f"Recent Choice: You made a decision")
    
    print("==========")


def load_scenarios(data_path: Path) -> Dict[int, List[Dict[str, Any]]]:
    """Load all scenario files."""
    scenarios = {}
    
    # Load each act
    for act_num in [1, 2, 3]:
        act_files = {
            1: "act1_mirrors.json",
            2: "act2_beasts.json", 
            3: "act3_whispers.json"
        }
        
        act_file = data_path / "scenarios" / act_files[act_num]
        if act_file.exists():
            with open(act_file, 'r', encoding='utf-8') as f:
                act_data = json.load(f)
                scenarios[act_num] = act_data.get("scenes", [])
        else:
            scenarios[act_num] = []
    
    return scenarios


def display_scene(scene: Dict[str, Any]) -> None:
    """Display a scene's text and atmosphere."""
    print(f"\n=== {scene.get('scene_id', 'Scene')} ===")
    print(scene.get("text", ""))
    print()


def get_player_choice(choices: List[Dict[str, Any]]) -> int:
    """Get player's choice from available options."""
    for i, choice in enumerate(choices, 1):
        text = choice['text']
        if choice.get('locked'):
            text += " [Locked]"
        print(f"{i}. {text}")
    
    while True:
        try:
            selection = input(f"\nChoose 1-{len(choices)}: ").strip()
            choice_idx = int(selection) - 1
            if 0 <= choice_idx < len(choices):
                if choices[choice_idx].get('locked'):
                    print("That path is sealed. Choose another option.")
                    continue
                return choice_idx
        except ValueError:
            pass
        print("Invalid choice. Please try again.")


def apply_choice_effects(state: Dict[str, Any], choice: Dict[str, Any], state_mgr: StateManager,
                         telemetry: Telemetry, debug_mode: bool = False) -> None:
    """Apply the psychological and state effects of a choice."""
    player_traits = state["player"]["traits"]

    # Normalize to canonical tag format if needed
    if "tags" not in choice:
        tag(
            choice,
            choice.get("primary_trait"),
            choice.get("primary_weight", 0.0),
            choice.get("secondary_trait"),
            choice.get("secondary_weight", 0.0),
        )

    for t in choice.get("tags", []):
        trait = t.get("trait")
        weight = t.get("weight", 0.0)
        if trait and weight > 0:
            player_traits[trait] = player_traits.get(trait, 0.0) + weight
    
    # Handle state flag setting
    flag_name = choice.get("set_flag")
    if flag_name:
        state_mgr.set_flag(flag_name, choice.get("flag_value", True))

    # Record the choice
    last_tags = choice.get("tags", [])
    state["last_choice"] = {
        "id": choice.get("choice_id", "unknown"),
        "primary_trait": last_tags[0]["trait"] if last_tags else None,
        "primary_weight": last_tags[0]["weight"] if last_tags else 0.0,
        "secondary_trait": last_tags[1]["trait"] if len(last_tags) > 1 else None,
        "secondary_weight": last_tags[1]["weight"] if len(last_tags) > 1 else 0.0,
    }
    
    # Log to telemetry
    telemetry.log({
        "event": "choice",
        "scene_id": choice.get("scene_id", "unknown"),
        "choice_id": choice.get("choice_id", "unknown"),
        "tags": last_tags,
    })
    
    # Show choice feedback based on mode
    if debug_mode and last_tags:
        print(f"\n[DEBUG] Choice effects:")
        for t in last_tags:
            print(f"  +{t['weight']} {t['trait']}")


def apply_scene_callbacks(scene: Dict[str, Any], state_mgr: StateManager) -> None:
    """Modify scene content based on state flags."""
    for cb in scene.get("callbacks", []):
        if state_mgr.check_flag(cb.get("flag"), cb.get("value", True)):
            if cb.get("text"):
                scene["text"] += " " + cb["text"]
            for change in cb.get("choices", []):
                for choice in scene.get("choices", []):
                    if choice.get("choice_id") == change.get("choice_id"):
                        choice.update({k: v for k, v in change.items() if k != "choice_id"})


def run_act(act_num: int, scenes: List[Dict[str, Any]], state: Dict[str, Any], state_mgr: StateManager,
           telemetry: Telemetry, show_hud_flag: bool, debug_mode: bool = False) -> bool:
    """Run through an act's scenes. Returns True if player wants to continue."""
    
    print(f"\n{'='*60}")
    print(f"ACT {act_num}: {['', 'MIRRORS', 'BEASTS', 'WHISPERS'][act_num]}")
    print(f"{'='*60}")
    
    if not scenes:
        print("No scenes available for this act.")
        return True
    
    # Show some scenes from this act (mix of scene types)
    scene_types = ["micro", "mid", "pocket"]
    available_scenes = [s for s in scenes if s.get("type") in scene_types]
    
    if not available_scenes:
        available_scenes = scenes[:3]  # Fallback to first few scenes
    
    # Select 3-4 scenes to play through
    num_scenes = min(4, len(available_scenes))
    selected_scenes = random.sample(available_scenes, num_scenes) if len(available_scenes) > num_scenes else available_scenes

    locked_added = False
    for scene in selected_scenes:
        if not locked_added:
            scene.setdefault("choices", []).append({
                "choice_id": "locked_fate",
                "text": "Attempt to escape your fate",
                "locked": True
            })
            locked_added = True

        apply_scene_callbacks(scene, state_mgr)

        if show_hud_flag:
            show_hud(state, debug_mode)

        display_scene(scene)
        
        choices = scene.get("choices", [])
        if not choices:
            print("No choices available. Moving on...")
            continue
        while len(choices) < 3:
            choices.append({
                "choice_id": f"wait_{len(choices)}",
                "text": "Hesitate, letting the moment pass.",
                "primary_trait": "Apathy",
                "primary_weight": 0.0
            })
            
        choice_idx = get_player_choice(choices)
        chosen = choices[choice_idx]
        
        apply_choice_effects(state, chosen, state_mgr, telemetry, debug_mode)
        
        print(f"\n> You chose: {chosen['text']}")
        
        # Add scene to completed list
        state["completed_scenes"].append(scene.get("scene_id", f"act{act_num}_scene"))
    
    # Ask if player wants to continue to next act
    if act_num < 3:
        print(f"\nAct {act_num} complete. Continue to Act {act_num + 1}?")
        choice = input("Continue? (y/n): ").strip().lower()
        return choice in ['y', 'yes', '']
    
    return True


def show_final_reflection(state: Dict[str, Any], data_path: Path) -> None:
    """Show the final psychological reflection."""
    print("\n" + "="*60)
    print("FINAL REFLECTION")
    print("="*60)
    
    reveals_path = data_path / "payoffs" / "endgame_reveals.json"
    
    if reveals_path.exists():
        reveal_data = load_reveals(reveals_path)
        reveal = pick_reveal(state["player"]["traits"], reveal_data)
        print("\n" + reveal["text"])
    else:
        # Fallback reflection
        traits = state["player"]["traits"]
        if traits:
            top_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"\nYour journey reveals these prominent traits:")
            for trait, value in top_traits:
                print(f"  {trait}: {value:.1f}")
            print(f"\nThrough your choices, {state['player']['name']}, you have shown who you truly are.")
        else:
            print(f"\nYour path through the labyrinth remains a mystery, {state['player']['name']}.")
            print("Perhaps some stories are meant to be lived, not analyzed.")


def main(argv: Any = None) -> int:
    """Main game loop."""
    parser = argparse.ArgumentParser(description="Janus v2-alpha RPG Engine")
    parser.add_argument("--load", help="Load game state from file")
    parser.add_argument("--save", help="Save game state to file")
    parser.add_argument("--no-hud", action="store_true", help="Disable HUD display")
    parser.add_argument("--debug", action="store_true", help="Enable developer debug mode (shows traits and weights)")
    parser.add_argument("--telemetry", help="Write telemetry events to file")
    args = parser.parse_args(argv)

    # Initialize game state
    state = default_state()
    if args.load:
        state = load_game(args.load)

    state_mgr = StateManager(state)
    telemetry = Telemetry(args.telemetry)
    data_path = Path(__file__).resolve().parent.parent / "data"
    
    # Get player name
    if state["player"]["name"] == "Adventurer":
        name = input("Enter your name: ").strip()
        state["player"]["name"] = name or "Adventurer"

    # Load all scenario content
    scenarios = load_scenarios(data_path)
    
    print(f"\nWelcome to the Labyrinth, {state['player']['name']}...")
    print("Your choices will shape both your story and reveal your true nature.")
    
    # Play through each act
    for act_num in range(state["current_act"], 4):
        state["current_act"] = act_num
        
        if not run_act(act_num, scenarios.get(act_num, []), state, state_mgr, telemetry, not args.no_hud, args.debug):
            print("\nYou choose to leave the labyrinth early...")
            break
    
    # Final processing
    if args.save:
        save_game(state, args.save)
    
    telemetry.save()
    
    if not args.no_hud:
        show_hud(state, args.debug)
    
    show_final_reflection(state, data_path)
    
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main())
