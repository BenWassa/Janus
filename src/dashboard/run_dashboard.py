import json
import random
import sys
from pathlib import Path
from typing import Dict, Any

from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px

# Ensure repository root is on path so we can import testing modules
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from testing import runner
from testing.policies import random_policy, hubris_forward, control_fear

DATA_DIR = ROOT / "data" / "test_results"

POLICIES = {
    "Seeded Random": random_policy.SeededRandomPolicy,
    "Hubris Forward": hubris_forward.HubrisForwardPolicy,
    "Control & Fear": control_fear.ControlFearPolicy,
}

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Janus Testing Dashboard"),
        html.Div(
            [
                dcc.Dropdown(
                    id="policy",
                    options=[{"label": name, "value": name} for name in POLICIES.keys()],
                    value="Seeded Random",
                ),
                html.Button("Run", id="run-btn", n_clicks=0),
            ],
            style={"maxWidth": "400px"},
        ),
        dcc.Graph(id="line-chart"),
        dcc.Graph(id="bar-chart"),
    ]
)

def _save_run(result: Dict[str, Any]) -> None:
    """Save run result to DATA_DIR with a sequential filename."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(DATA_DIR.glob("run_*.json"))
    fname = DATA_DIR / f"run_{len(existing) + 1}.json"
    data = {
        "decisions_made": sum(1 for e in result["trace"] if not e.get("end")),
        "trait_progression": result["trace"],
        "final_traits": result["final"]["normalized"],
        "final_reveal": result["final"].get("top3", []),
    }
    with fname.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

def _build_figures(result: Dict[str, Any]):
    """Return line and bar chart figures for a result."""
    line_rows = []
    for entry in result["trace"]:
        if entry.get("end"):
            continue
        step = entry["step"]
        for trait, total in entry["totals"].items():
            line_rows.append({"step": step, "trait": trait, "total": total})
    line_fig = px.line(line_rows, x="step", y="total", color="trait")

    final = result["final"]["normalized"]
    bar_fig = px.bar(x=list(final.keys()), y=list(final.values()))
    bar_fig.update_layout(xaxis_title="Trait", yaxis_title="Score")

    return line_fig, bar_fig

@app.callback(
    [Output("line-chart", "figure"), Output("bar-chart", "figure")],
    Input("run-btn", "n_clicks"),
    State("policy", "value"),
    prevent_initial_call=True,
)
def run_simulation(n_clicks: int, policy_name: str):
    policy_cls = POLICIES[policy_name]
    policy = policy_cls()
    result = runner.run(policy, seed=random.randint(0, 1_000_000))
    _save_run(result)
    return _build_figures(result)

if __name__ == "__main__":
    app.run_server(debug=True)
