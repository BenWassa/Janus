HUMILITY_HUBRIS_KEY = "hh_score"
BUCKETS = {
    "excess_humility": range(-5, -2),
    "balanced": range(-2, 3),
    "excess_hubris": range(3, 6),
}

def init_trait(traits: dict):
    traits.setdefault(HUMILITY_HUBRIS_KEY, 0)

def apply_delta(traits: dict, delta: int):
    traits[HUMILITY_HUBRIS_KEY] = max(-5, min(5, traits.get(HUMILITY_HUBRIS_KEY, 0) + delta))
    return traits[HUMILITY_HUBRIS_KEY]

def bucket_for(value: int) -> str:
    for name, r in BUCKETS.items():
        if value in r:
            return name
    return "balanced"
