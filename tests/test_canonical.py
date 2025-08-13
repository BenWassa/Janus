import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from analytics import canonicalize, normalize_traits


def test_canonicalize_maps_duplicates():
    assert canonicalize("Control & Perfectionism") == "Control"
    assert canonicalize("Apathy & Sloth") == "Apathy"
    assert canonicalize("Pessimism & Cynicism") == "Cynicism"
    assert canonicalize("Cynicism") == "Cynicism"
    assert canonicalize("Moodiness & Indirectness") == "Moodiness"


def test_canonicalize_unknown_raises():
    with pytest.raises(ValueError):
        canonicalize("Unknown Trait")


def test_normalize_traits_merges_duplicates():
    data = {"Control & Perfectionism": 1.0, "Control": 2.0}
    norm = normalize_traits(data)
    assert norm["Control"] == 3.0
    assert "Control & Perfectionism" not in norm
