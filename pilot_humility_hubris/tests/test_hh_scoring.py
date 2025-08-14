from pilot_humility_hubris.continuum import init_trait, apply_delta

def test_bounds():
    state = {"traits": {}}
    init_trait(state["traits"])
    apply_delta(state["traits"], 10)
    assert state["traits"]["hh_score"] == 5
    apply_delta(state["traits"], -20)
    assert state["traits"]["hh_score"] == -5
