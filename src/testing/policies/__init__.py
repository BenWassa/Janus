"""Collection of scripted decision policies for the testing harness."""

from .random_policy import SeededRandomPolicy
from .hubris_forward import HubrisForwardPolicy
from .control_fear import ControlFearPolicy
from .deception_avarice import DeceptionAvaricePolicy
from .reckless_chaotic import RecklessChaoticPolicy
from .balanced_human import BalancedHumanPolicy


POLICIES = {
    "random": SeededRandomPolicy,
    "hubris": HubrisForwardPolicy,
    "control_fear": ControlFearPolicy,
    "deception_avarice": DeceptionAvaricePolicy,
    "reckless_chaotic": RecklessChaoticPolicy,
    "balanced_human": BalancedHumanPolicy,
}


__all__ = ["POLICIES"]

