from .continuum import HUMILITY_HUBRIS_KEY, bucket_for

def render_hh_paragraph(state: dict) -> str:
    score = state["traits"].get(HUMILITY_HUBRIS_KEY, 0)
    bucket = bucket_for(score)
    if bucket == "excess_humility":
        return "In the Chronicle you walk with lowered gaze—gentle, careful, sometimes smaller than your shadow."
    if bucket == "excess_hubris":
        return "In the Chronicle you stride high-crowned—decisive, daring, sometimes louder than your truth."
    return "In the Chronicle you move with steady regard—neither inflated nor diminished by the Labyrinth’s gaze."
