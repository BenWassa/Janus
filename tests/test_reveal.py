from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from modules.reveal import load_reveals, pick_reveal

REVEALS_PATH = Path(__file__).resolve().parents[1] / "data" / "payoffs" / "endgame_reveals.json"


def test_hubris_control_reveal():
    reveals = load_reveals(REVEALS_PATH)
    text = pick_reveal({"Hubris": 1.0, "Control": 0.5}, reveals)["text"]
    assert "Hubris" in text and "Control" in text


def test_avarice_wrath_reveal():
    reveals = load_reveals(REVEALS_PATH)
    text = pick_reveal({"Avarice": 1.2, "Wrath": 0.7}, reveals)["text"]
    assert "Avarice" in text and "Wrath" in text


def test_tied_traits_use_fallback():
    reveals = load_reveals(REVEALS_PATH)
    text = pick_reveal({"Hubris": 0.5, "Avarice": 0.5}, reveals)["text"]
    assert "glass offers no single emblem" in text
