#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Labyrinth of Three Doors — Pilot (Single-File)
Console RPG with a minimalist HUD using Rich.
Tested with Python 3.10+
pip install rich
Run: python labyrinth_rpg_pilot.py
"""

from __future__ import annotations
import sys, textwrap
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.box import ROUNDED

WIDTH = 76  # keep lines under this width to avoid horizontal scroll
console = Console(width=WIDTH)

def wrap(s: str) -> str:
    return textwrap.fill(s, width=WIDTH-2)

HEARTS = ["", "♥", "♥♥", "♥♥♥", "♥♥♥♥"]
DOTS = {0: "○○○", 1: "●○○", 2: "●●○", 3: "●●●"}

@dataclass
class Player:
    name: str = "???"
    hp: int = 4  # 1..4 hearts
    bravery: int = 1
    cunning: int = 1
    chaos: int = 1
    items: List[str] = field(default_factory=list)

    def stat_panel(self) -> Panel:
        items_txt = ", ".join(self.items) if self.items else "None"
        text = Text.assemble(
            ("[Name: ", "cyan"),
            (self.name, "bold cyan"),
            ("]   HP: ", "cyan"),
            (HEARTS[self.hp], "red"),
            ("  |  Bravery: ", "cyan"),
            (DOTS[self.bravery], "yellow"),
            ("  Cunning: ", "cyan"),
            (DOTS[self.cunning], "yellow"),
            ("  Chaos: ", "cyan"),
            (DOTS[self.chaos], "yellow"),
            ("\nItems: ", "cyan"),
            (f"[{items_txt}]", "green"),
        )
        return Panel(text, title="HUD", title_align="left", box=ROUNDED)

@dataclass
class Scene:
    key: str
    title: str
    description: str
    choices: Dict[str, str]  # label -> next_scene_key
    on_enter: Optional[callable] = None  # function(player) -> None
    wind: str = "Still"
    nearby: str = ""

class Game:
    def __init__(self):
        self.player = Player()
        self.scenes: Dict[str, Scene] = {}
        self.current: str = "antechamber"
        self.ended: bool = False

    def add_scene(self, scene: Scene):
        self.scenes[scene.key] = scene

    def render_scene(self, scene: Scene):
        # Optional: adapt wrapping to live console width
        width = console.size.width
        wrapped = "\n".join(textwrap.wrap(scene.description, max(30, width - 6)))

        # Clear and print HUD
        console.clear()
        console.print(self.player.stat_panel())

        # Build body (atmosphere + title + description) and print
        atmos = f"Wind: {scene.wind}\nNearby: {scene.nearby}" if scene.nearby else f"Wind: {scene.wind}"
        body_text = Text()
        body_text.append(atmos + "\n", style="magenta")
        body_text.append("───── ✦ ─────\n", style="dim")
        body_text.append(scene.title + "\n\n", style="bold underline")
        wrapped = "\n".join(textwrap.wrap(scene.description, WIDTH - 2))
        body_text.append(wrapped)
        console.print(Panel(body_text, box=ROUNDED))

        # Choices panel
        tbl = Table(show_header=False, box=ROUNDED, expand=True, padding=(0, 1))
        for i, label in enumerate(scene.choices.keys(), start=1):
            tbl.add_row(f"{i}. {label}")
        console.print(Panel(tbl, title="What do you do?", title_align="left", box=ROUNDED))


    def get_choice(self, scene: Scene) -> str:
        labels = list(scene.choices.keys())
        while True:
            try:
                console.print("\nEnter choice number:", style="bold cyan")
                s = input("> ").strip()
                idx = int(s) - 1
                if 0 <= idx < len(labels):
                    return scene.choices[labels[idx]]
            except Exception:
                pass
            console.print("Invalid choice. Try again.", style="red")

    def run(self):
        while not self.ended:
            scene = self.scenes[self.current]
            if scene.on_enter:
                scene.on_enter(self.player)
            self.render_scene(scene)
            next_key = self.get_choice(scene)
            if next_key.startswith("END:"):
                self.end_game(next_key[4:])
                break
            self.current = next_key

    def end_game(self, ending_key: str):
        endings = {
            "HEROIC": "You carry a quiet light out of the labyrinth and into a dawn that feels like your name.",
            "TRAGIC": "The mirrors close over you like water. Somewhere, another you makes a better choice.",
            "ABSURD": "A chorus of crows knights you with a spoon. Technically a victory. Emotionally questionable.",
            "MYSTERIOUS": "A door opens to a door opens to a door. You step through, smiling. Some riddles are homes.",
            "COMEDIC": "You trip on destiny, land on a treasure chest, and somehow invent stairs. Everyone cheers.",
            "BITTERSWEET": "You free a friend you cannot follow. The lantern burns on without you.",
        }
        msg = endings.get(ending_key, "The story folds itself up like a map and tucks you into a pocket universe.")
        self.ended = True
        console.clear()
        panel = Panel(
            Align.center(Text(msg + "\n\n[Press Enter to exit]", justify="center"), vertical="middle"),
            title=f"Ending — {ending_key}", width=WIDTH, box=ROUNDED
        )
        console.print(panel)
        input()

# --- Scene logic callbacks ----------------------------------------------------

def pick_up_lantern(player: Player):
    if "Lantern" not in player.items:
        player.items.append("Lantern")
        player.bravery = min(3, player.bravery + 1)

def mirror_gain_shard(player: Player):
    if "Mirror Shard" not in player.items:
        player.items.append("Mirror Shard")
        player.cunning = min(3, player.cunning + 1)

def beasts_mark(player: Player):
    if "Beast Token" not in player.items:
        player.items.append("Beast Token")
        player.bravery = min(3, player.bravery + 1)

def whispers_mark(player: Player):
    if "Whisper Key" not in player.items:
        player.items.append("Whisper Key")
        player.chaos = min(3, player.chaos + 1)

# --- Build Game ---------------------------------------------------------------

def build_game() -> Game:
    g = Game()

    g.add_scene(Scene(
        key="antechamber",
        title="Scene 1 — The Antechamber",
        description=(
            "You awaken on black-and-white tiles that hum beneath your touch. Three doors stand ahead: "
            "the Door of Mirrors (liquid silver), the Door of Beasts (carved with wolves and crows), "
            "and the Door of Whispers (plain wood, yet somehow calling your name). A dust-covered lantern "
            "flickers at your feet."
        ),
        wind="Cold, from the East",
        nearby="A faint scratching at the far wall",
        choices={
            "Pick up the lantern": "take_lantern",
            "Step through the Door of Mirrors": "mirrors_1",
            "Push open the Door of Beasts": "beasts_1",
            "Approach the Door of Whispers": "whispers_1",
        }
    ))

    g.add_scene(Scene(
        key="take_lantern",
        title="You Take the Lantern",
        description=(
            "The glass is smudged but warm in your hand. When you tilt it, the flame tilts too, like it's listening. "
            "Its light makes the room feel smaller, safer—or perhaps just more honest."
        ),
        choices={
            "Go to the Door of Mirrors": "mirrors_1",
            "Go to the Door of Beasts": "beasts_1",
            "Go to the Door of Whispers": "whispers_1",
        },
        on_enter=pick_up_lantern,
        wind="Cold, now steady",
        nearby="The scratching pauses, as if surprised"
    ))

    # Mirrors path
    g.add_scene(Scene(
        key="mirrors_1",
        title="Door of Mirrors",
        description=(
            "Silver ripples under your palm. Your reflection splits into three: cautious, clever, and chaotic. "
            "Only one steps when you step. The others wait."
        ),
        choices={
            "Touch the still reflection": "mirrors_still",
            "Touch the clever reflection": "mirrors_clever",
            "Ignore them and step through": "mirrors_deeper",
        },
        wind="None",
        nearby="A soft chime from nowhere"
    ))

    g.add_scene(Scene(
        key="mirrors_still",
        title="The Still Reflection",
        description=(
            "Your hand meets cool glass. The still one smiles and hands you a shard—your face, but braver. "
            "It pricks your finger; a single drop wakes the mirror."
        ),
        choices={
            "Take the shard and proceed": "mirrors_deeper",
            "Back away carefully": "antechamber",
        },
        on_enter=mirror_gain_shard
    ))

    g.add_scene(Scene(
        key="mirrors_clever",
        title="The Clever Reflection",
        description=(
            "It moves before you do and mouths a warning: 'Count the doors behind the doors.' "
            "When you blink, it becomes a shard in your hand."
        ),
        choices={
            "Pocket the shard and proceed": "mirrors_deeper",
            "Return to the start": "antechamber",
        },
        on_enter=mirror_gain_shard
    ))

    g.add_scene(Scene(
        key="mirrors_deeper",
        title="Hall of Unchosen Days",
        description=(
            "You step into a corridor of possibilities. Each mirror shows a life you could have lived. "
            "Some smile at you; some look away. A thin path winds between them."
        ),
        choices={
            "Break a mirror to free a life": "mirrors_break",
            "Walk the thin path without touching anything": "mirrors_path",
            "Use the Lantern to search for a true door": "mirrors_lantern",
        },
        wind="Still, heavy",
        nearby="Distant footsteps that match your heartbeat"
    ))

    g.add_scene(Scene(
        key="mirrors_break",
        title="Shards Like Stars",
        description=(
            "Glass bursts like starlight. A freed life gasps and runs past you, laughing—your laugh, "
            "from a different decade. The mirrors darken. A door opens."
        ),
        choices={
            "Step through the new door": "END:BITTERSWEET",
            "Stay and break more mirrors": "END:ABSURD",
        }
    ))

    g.add_scene(Scene(
        key="mirrors_path",
        title="The Narrow Way",
        description=(
            "You balance between possible selves. Your breath fogs the glass. At the end, a mirror "
            "shows you now—tired, but certain."
        ),
        choices={
            "Step into yourself": "END:HEROIC",
            "Turn back at the last second": "antechamber",
        }
    ))

    g.add_scene(Scene(
        key="mirrors_lantern",
        title="Lamplight Test",
        description=(
            "You raise the lantern. Some mirrors dim; one grows warmer. In its glow, you see a version of you "
            "holding a key made of sound."
        ),
        choices={
            "Reach through and take the key": "END:MYSTERIOUS",
            "Look away and walk on": "mirrors_path",
        }
    ))

    # Beasts path
    g.add_scene(Scene(
        key="beasts_1",
        title="Door of Beasts",
        description=(
            "A forest corridor blinks awake. A wolf with cold eyes, a crow on its back, and a sleepily coiled snake "
            "watch you like judges at a quiet trial."
        ),
        choices={
            "Bow to the animals": "beasts_bow",
            "Stare back without fear": "beasts_stare",
            "Offer the lantern's warmth": "beasts_offer_lantern",
        },
        wind="Pine-scented",
        nearby="Leaves counting themselves"
    ))

    g.add_scene(Scene(
        key="beasts_bow",
        title="Old Courtesy",
        description=(
            "You bow. The wolf nods once; the crow caws an approval you feel in your bones. The snake gifts a token, "
            "rough as bark."
        ),
        choices={
            "Take the Beast Token and follow": "beasts_follow",
            "Refuse the token and leave": "antechamber",
        },
        on_enter=beasts_mark
    ))

    g.add_scene(Scene(
        key="beasts_stare",
        title="Trial by Gaze",
        description=(
            "You stare into the wolf's eyes. They are a winter river. Something inside you steadies—or cracks."
        ),
        choices={
            "Hold the gaze": "END:TRAGIC",
            "Blink and step back": "beasts_1",
        }
    ))

    g.add_scene(Scene(
        key="beasts_offer_lantern",
        title="Shared Warmth",
        description=(
            "You set the lantern down. The animals gather around it like a small parliament. The crow taps the glass, "
            "grinning. 'Friend,' it says, and means it."
        ),
        choices={
            "Ask them to guide you": "beasts_follow",
            "Take the lantern back and leave": "antechamber",
        },
        on_enter=beasts_mark
    ))

    g.add_scene(Scene(
        key="beasts_follow",
        title="Path of Quiet Footsteps",
        description=(
            "They lead you through ferns to a hill of doors. 'Choose with your feet,' the crow suggests. "
            "Your soles know the answer before your mind does."
        ),
        choices={
            "Follow your feet to the low door": "END:COMEDIC",
            "Climb to the highest door with the wolf": "END:HEROIC",
        }
    ))

    # Whispers path
    g.add_scene(Scene(
        key="whispers_1",
        title="Door of Whispers",
        description=(
            "Plain wood, worn smooth by other hands. A voice you trust—your own?—speaks from the keyhole: "
            "'Not every secret is a trap. Some are ladders.'"
        ),
        choices={
            "Whisper your true name": "whispers_true",
            "Lie about your name": "whispers_lie",
            "Listen without speaking": "whispers_listen",
        },
        wind="Draft through the cracks",
        nearby="A soft ticking like a heart in a box"
    ))

    g.add_scene(Scene(
        key="whispers_true",
        title="Key of Honesty",
        description=(
            "You whisper your name. The door warms under your palm. A key shapes itself from the whisper and falls into "
            "your hand."
        ),
        choices={
            "Take the Whisper Key and open the door": "whispers_open",
            "Pocket the key and retreat": "antechamber",
        },
        on_enter=whispers_mark
    ))

    g.add_scene(Scene(
        key="whispers_lie",
        title="Mask of Echoes",
        description=(
            "You speak a false name. The door opens anyway. Inside, you hear two sets of footsteps: yours and the mask's."
        ),
        choices={
            "Enter boldly": "END:ABSURD",
            "Abandon the lie and start again": "whispers_1",
        }
    ))

    g.add_scene(Scene(
        key="whispers_listen",
        title="Patience at the Threshold",
        description=(
            "You listen until the ticking matches your pulse. A hidden latch clicks. 'Very well,' the door sighs."
        ),
        choices={
            "Slip inside": "whispers_open",
            "Turn away, uneasy": "antechamber",
        }
    ))

    g.add_scene(Scene(
        key="whispers_open",
        title="Room of Promises",
        description=(
            "Candles, a table, a single contract with your handwriting already on it. It promises courage you do not yet "
            "have, to a person you have not yet met."
        ),
        choices={
            "Sign it and mean it": "END:HEROIC",
            "Burn it with the lantern": "END:MYSTERIOUS",
        }
    ))

    return g

if __name__ == "__main__":
    game = build_game()
    try:
        game.run()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Game interrupted.[/bold red]")
