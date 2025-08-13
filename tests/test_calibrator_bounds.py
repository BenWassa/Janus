"""Tests for the Calibrator configuration bounds."""
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.calibrator.calibrator import Calibrator


def _base_config(overrides=None):
    cfg = {
        "multipliers": {},
        "anti_streak": 0.15,
        "decay": 0.03,
        "scene_cap": 0.5,
        "act_cap": 1.5,
        "epsilon": 0.03,
    }
    if overrides:
        cfg.update(overrides)
    return cfg


def test_multiplier_clamped() -> None:
    calib = Calibrator(_base_config({"multipliers": {"courage": 0.5}}))
    assert calib.multipliers["courage"] == 0.8

    calib = Calibrator(_base_config({"multipliers": {"courage": 3.0}}))
    assert calib.multipliers["courage"] == 2.0


def test_anti_streak_and_decay() -> None:
    config = _base_config({"multipliers": {"courage": 1.0}})
    calib = Calibrator(config)
    history = ["courage", "courage"]
    mult = calib.calibrate(history, "courage")
    expected = 1.0 * (1 - config["anti_streak"]) * (1 - config["decay"])
    assert abs(mult - expected) < 1e-6


def test_epsilon_bound() -> None:
    calib = Calibrator(_base_config({"epsilon": 0.05}))
    assert calib.epsilon == 0.03
