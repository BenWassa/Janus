from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from modules.scoring import normalize_scores, top_archetype


def test_normalize_scores():
    scores = normalize_scores({"Hubris": 2.0, "Fear": 1.0})
    assert abs(scores["Hubris"] - 2/3) < 1e-6
    assert abs(scores["Fear"] - 1/3) < 1e-6


def test_top_archetype():
    name, desc = top_archetype({"Avarice": 3.0, "Fear": 1.0})
    assert name == "The Collector"
    assert "glitters" in desc


def test_combo_archetype():
    traits = {"self_reflection": 2.0, "restraint": 1.5, "aggression": 0.5}
    name, desc = top_archetype(traits)
    assert name == "The Harmonizer"
    assert "balance" in desc
