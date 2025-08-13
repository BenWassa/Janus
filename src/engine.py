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
from modules.state_manager import StateManager
from modules.scoring import top_archetype
from modules.symbols import describe as describe_symbol


def default_state() -> Dict[str, Any]:
    """Initial game state."""
    return {
        "player": {"name": "Adventurer"},
        "current_act": 1,
        "current_scene": 0,
        "completed_scenes": [],
        "last_choice": None,
        "memory": {
            "state_flags": {"mirror": None, "beast": None, "storm": None},
            "trait_scores": {},
            "decision_log": [],
        },
    }


def show_hud(state: Dict[str, Any], debug_mode: bool = False) -> None:
    """Display game HUD with player status."""
    if debug_mode:
        print("== DEBUG HUD ==")
        print(f"Player: {state['player']['name']}")
        print(f"Act: {state['current_act']}")

        # Show traits if any exist (debug only)
        traits = state["memory"]["trait_scores"]
        if traits:
            for trait, value in sorted(traits.items()):
                print(f"  {trait}: {value:.1f}")

        # Show flags if any exist (debug only)
        flags = state["memory"].get("state_flags", {})
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

    # Trait scoring
    impacts = choice.get("traits_impact")
    if impacts:
        for trait, weight in impacts.items():
            state_mgr.add_trait(trait, weight)
    else:
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
            if trait:
                state_mgr.add_trait(trait, weight)
    
    # Handle state flag setting
    flag_name = choice.get("set_flag")
    if flag_name:
        state_mgr.set_flag(flag_name, choice.get("flag_value", True))
        recap = choice.get("recap", choice.get("text", "")).strip()
        state["memory"]["decision_log"].append(recap)

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


def apply_state_variations(scene: Dict[str, Any], act_num: int, state_mgr: StateManager) -> None:
    """Inject simple narrative variations based on stored flags."""
    mirror = state_mgr.get_flag("mirror")
    beast = state_mgr.get_flag("beast")
    if act_num >= 2:
        if mirror == "disturbed":
            scene["text"] += " The memory of rippled glass unsettles you." 
        elif mirror == "observed":
            scene["text"] += " The mirror's calm steadies your resolve."
    if act_num >= 3:
        if beast == "spared":
            scene["text"] += " A grateful beast's shadow follows."
        elif beast == "slain":
            scene["text"] += " The cry of a slain beast echoes at your back."


def apply_symbol_rules(scene: Dict[str, Any], state_mgr: StateManager) -> None:
    """Modify symbol scenes based on dominant related traits."""
    symbol = scene.get("symbol")
    if not symbol:
        return
    desc = describe_symbol(symbol, state_mgr.trait_scores)
    if desc:
        scene["text"] += f" {desc}"


def act_intro(act_num: int, state_mgr: StateManager) -> None:
    """Print an act introduction referencing prior flags."""
    mirror = state_mgr.get_flag("mirror")
    beast = state_mgr.get_flag("beast")
    if act_num == 1:
        print("You stand before endless mirrors, the journey begins.")
    elif act_num == 2:
        if mirror == "disturbed":
            print("Ripples from the mirror pool guide your steps toward the beasts.")
        elif mirror == "observed":
            print("The still mirror lends you quiet focus as beasts stir ahead.")
        else:
            print("Memories of mirrored halls fade as beasts emerge.")
    elif act_num == 3:
        line = "Whispers rise around you"
        if beast == "spared":
            line += ", and the beast you spared pads nearby"
        elif beast == "slain":
            line += ", though the beast you slew haunts your thoughts"
        print(line + ".")


def act_interlude(act_num: int, state_mgr: StateManager) -> None:
    """Summarise key prior actions between acts."""
    mirror = state_mgr.get_flag("mirror")
    beast = state_mgr.get_flag("beast")
    if act_num == 1:
        if mirror == "disturbed":
            print("A brief calm settles as the mirror's ripples fade.")
        elif mirror == "observed":
            print("Silence rewards your patience before the mirror.")
        else:
            print("You leave the mirrors without a trace.")
    elif act_num == 2:
        if beast == "spared":
            print("The spared beast watches over your path ahead.")
        elif beast == "slain":
            print("The memory of the beast you slew weighs on you.")
        else:
            print("No beast chose to follow you onward.")


def run_act(act_num: int, scenes: List[Dict[str, Any]], state: Dict[str, Any], state_mgr: StateManager,
           telemetry: Telemetry, show_hud_flag: bool, debug_mode: bool = False) -> bool:
    """Run through an act's scenes. Returns True if player wants to continue."""

    print(f"\n{'='*60}")
    print(f"ACT {act_num}: {['', 'MIRRORS', 'BEASTS', 'WHISPERS'][act_num]}")
    print(f"{'='*60}")

    act_intro(act_num, state_mgr)
    
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
        apply_state_variations(scene, act_num, state_mgr)
        apply_symbol_rules(scene, state_mgr)

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
        act_interlude(act_num, state_mgr)
        print(f"\nAct {act_num} complete. Continue to Act {act_num + 1}?")
        choice = input("Continue? (y/n): ").strip().lower()
        return choice in ['y', 'yes', '']

    return True


def generate_decision_recap(state: Dict[str, Any]) -> str:
    """Return a short recap of pivotal decisions based on state flags."""
    decisions = state["memory"].get("decision_log", [])
    if not decisions:
        return ""
    selected = decisions[:4]
    parts = [d.rstrip('.') for d in selected]
    return "You " + ", then you ".join(parts) + "."


def generate_final_epilogue(state_mgr: StateManager) -> str:
    """Compose a symbolic epilogue using stored flags and trait scores."""
    parts: List[str] = []
    traits = state_mgr.trait_scores
    for symbol, value in state_mgr.state_flags.items():
        if value:
            desc = describe_symbol(symbol, traits)
            if desc:
                parts.append(desc)
    return " ".join(parts)


def show_heros_chronicle(state: Dict[str, Any], state_mgr: StateManager) -> None:
    """Output the final Hero's Chronicle summary."""
    print("\n=== Hero's Chronicle ===")
    recap = generate_decision_recap(state)
    if recap:
        print(recap)
    archetype_name, archetype_desc = top_archetype(state_mgr.trait_scores)
    print(f"{archetype_name}: {archetype_desc}")
    epilogue = generate_final_epilogue(state_mgr)
    if epilogue:
        print(epilogue)


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

    show_heros_chronicle(state, state_mgr)
    
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main())
