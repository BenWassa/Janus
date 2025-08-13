"""Calibration utilities for policy tuning."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


def _clamp(value: float, low: float, high: float) -> float:
    """Clamp *value* to the inclusive range [low, high]."""
    return max(low, min(high, value))


@dataclass
class Calibrator:
    """Applies bounded multipliers and simple dampening rules."""

    config: Dict[str, float | Dict[str, float]]
    multipliers: Dict[str, float] = field(init=False)
    anti_streak: float = field(init=False)
    decay: float = field(init=False)
    scene_cap: float = field(init=False)
    act_cap: float = field(init=False)
    epsilon: float = field(init=False)

    def __post_init__(self) -> None:
        mults = self.config.get("multipliers", {})
        self.multipliers = {k: _clamp(v, 0.8, 2.0) for k, v in mults.items()}
        self.anti_streak = _clamp(self.config.get("anti_streak", 0.15), 0.0, 0.15)
        self.decay = _clamp(self.config.get("decay", 0.03), 0.0, 0.03)
        self.scene_cap = _clamp(self.config.get("scene_cap", 0.5), 0.0, 0.5)
        self.act_cap = _clamp(self.config.get("act_cap", 1.5), 0.0, 1.5)
        self.epsilon = _clamp(self.config.get("epsilon", 0.03), 0.0, 0.03)

    def calibrate(self, history: List[str], trait: str) -> float:
        """Return calibrated multiplier for *trait* given selection *history*.

        The multiplier is bounded and applies anti-streak dampening for
        consecutive selections of the same trait as well as a per-step decay.
        """
        mult = self.multipliers.get(trait, 1.0)

        # Anti-streak: if the last two selections match the current trait,
        # dampen the multiplier by the configured percentage.
        if len(history) >= 2 and history[-1] == history[-2] == trait:
            mult *= 1.0 - self.anti_streak

        # Apply per-step decay.
        mult *= 1.0 - self.decay

        # Enforce act-wide cap (scene caps require external tracking).
        mult = _clamp(mult, 0.0, self.act_cap)
        return mult
