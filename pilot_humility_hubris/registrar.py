import os, json
from .continuum import init_trait
from .symbol_variants import render_mirror_variant
from .payoff_hook import render_hh_paragraph

def attach(runtime):
    init_trait(runtime.state["traits"])
    patches_dir = os.path.join(os.path.dirname(__file__), "scene_patches")
    for fname in os.listdir(patches_dir):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(patches_dir, fname), encoding="utf-8") as fh:
            patch = json.load(fh)
            runtime.scenes.register_patch(patch["scene_id"], patch, continuum_key="humility_hubris")
    runtime.symbols.register_variant("mirror", render_mirror_variant)
    runtime.payoff.register_epilogue_paragraph(render_hh_paragraph)
