"""Tests for the Optimizer objective scoring."""
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.calibrator.optimizer import Optimizer


def test_score_penalizes_deviation_and_intent() -> None:
    score_lock = Optimizer.score(balance=0.6, deviation=0.2, intent_lock=True)
    score_no_lock = Optimizer.score(balance=0.6, deviation=0.2, intent_lock=False)
    assert score_lock > score_no_lock

    score_worse_balance = Optimizer.score(balance=0.4, deviation=0.2, intent_lock=True)
    assert score_lock > score_worse_balance


def test_optimizer_selects_highest_score() -> None:
    candidates = {
        "a": {"config": {"x": 1}, "balance": 0.5, "policy_deviation": 0.4, "intent_lock": True},
        "b": {"config": {"x": 2}, "balance": 0.6, "policy_deviation": 0.2, "intent_lock": True},
    }
    opt = Optimizer()
    config, stats = opt.optimize(candidates)
    assert config == {"x": 2}
    assert stats["balance"] == 0.6
