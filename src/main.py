import os
import sys
from types import SimpleNamespace

# Add workspace root to sys.path for top-level imports
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
# ensure engine and its submodules can be imported
sys.path.append(os.path.dirname(__file__))
import engine

def main(argv=None):
    runtime = SimpleNamespace(
        state={"traits": {}},
        scenes=SimpleNamespace(register_patch=lambda *a, **k: None),
        symbols=SimpleNamespace(register_variant=lambda *a, **k: None),
        payoff=SimpleNamespace(register_epilogue_paragraph=lambda func: None),
    )
    if os.getenv("JANUS_PILOT_HH") == "1":
        from pilot_humility_hubris.registrar import attach
        attach(runtime)
    return engine.main(argv)

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
