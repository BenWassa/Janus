from .continuum import HUMILITY_HUBRIS_KEY, bucket_for

def render_mirror_variant(state: dict) -> str:
    score = state["traits"].get(HUMILITY_HUBRIS_KEY, 0)
    b = bucket_for(score)
    if b == "excess_humility":
        return "The mirror dims; your outline seems smaller than it should be."
    if b == "excess_hubris":
        return "The mirror swells your form, as though the world tilts around you."
    return "The mirror shows you as you are—neither magnified nor diminished."
