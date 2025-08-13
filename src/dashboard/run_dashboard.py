import json
import subprocess
import sys
import os

# Ensure required packages are installed
def install_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_path])

install_requirements()
import random
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

# Initialize with empty charts
def get_initial_charts():
    """Create initial empty charts."""
    empty_line = px.line()
    empty_bar = px.bar()
    for fig in [empty_line, empty_bar]:
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E7EBFF',
            title="Click 'Run Simulation' to generate charts",
            title_font_color='#8A90A2'
        )
    return empty_line, empty_bar

app = Dash(__name__, assets_folder='assets')

app.layout = html.Div(
    [
        html.H1("🚪 Janus Testing Dashboard", style={"textAlign": "center", "marginBottom": "2rem"}),
        
        # Control Panel
        html.Div([
            html.H2("Control Panel"),
            html.Div([
                html.Label("Policy Selection:"),
                dcc.Dropdown(
                    id="policy",
                    options=[{"label": name, "value": name} for name in POLICIES.keys()],
                    value="Seeded Random",
                    style={"marginBottom": "1rem", "width": "300px"}
                ),
                html.Button("▶ Run Simulation", id="run-btn", n_clicks=0, 
                           style={"backgroundColor": "#6AA6FF", "color": "white", "border": "none", 
                                  "borderRadius": "8px", "padding": "10px 20px", "cursor": "pointer"}),
                html.Div(id="status", style={"marginTop": "10px", "color": "#8A90A2"}),
            ])
        ], style={"backgroundColor": "#151821", "border": "1px solid rgba(255,255,255,0.06)", 
                  "borderRadius": "12px", "padding": "20px", "marginBottom": "20px"}),
        
        # Results Section
        html.Div([
            html.H2("Results"),
            dcc.Graph(id="line-chart", figure=get_initial_charts()[0]),
            dcc.Graph(id="bar-chart", figure=get_initial_charts()[1]),
        ], style={"backgroundColor": "#151821", "border": "1px solid rgba(255,255,255,0.06)", 
                  "borderRadius": "12px", "padding": "20px"})
    ],
    style={"backgroundColor": "#0F1115", "color": "#E7EBFF", "minHeight": "100vh", 
           "padding": "20px", "fontFamily": "Inter, sans-serif"}
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
    try:
        line_rows = []
        for entry in result["trace"]:
            if entry.get("end"):
                continue
            step = entry["step"]
            for trait, total in entry["totals"].items():
                line_rows.append({"step": step, "trait": trait, "total": total})
        
        # Create line chart with dark theme
        if line_rows:
            line_fig = px.line(line_rows, x="step", y="total", color="trait")
        else:
            line_fig = px.line()
            
        line_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E7EBFF',
            title="Trait Progression Over Time",
            title_font_size=16,
            title_font_color='#6AA6FF'
        )
        line_fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        line_fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')

        final = result.get("final", {}).get("normalized", {})
        
        # Create bar chart with dark theme
        if final:
            bar_fig = px.bar(x=list(final.keys()), y=list(final.values()))
        else:
            bar_fig = px.bar()
            
        bar_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E7EBFF',
            xaxis_title="Trait", 
            yaxis_title="Final Score",
            title="Final Trait Scores",
            title_font_size=16,
            title_font_color='#6AA6FF'
        )
        bar_fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        bar_fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
        bar_fig.update_traces(marker_color='#6AA6FF')

        return line_fig, bar_fig
    
    except Exception as e:
        # Return empty charts if there's an error
        empty_line = px.line()
        empty_bar = px.bar()
        for fig in [empty_line, empty_bar]:
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#E7EBFF',
                title=f"Error: {str(e)}",
                title_font_color='#FF5B5B'
            )
        return empty_line, empty_bar

@app.callback(
    [Output("line-chart", "figure"), Output("bar-chart", "figure"), Output("status", "children")],
    Input("run-btn", "n_clicks"),
    State("policy", "value"),
    prevent_initial_call=True,
)
def run_simulation(n_clicks: int, policy_name: str):
    try:
        if not policy_name or policy_name not in POLICIES:
            raise ValueError(f"Invalid policy: {policy_name}")
            
        policy_cls = POLICIES[policy_name]
        policy = policy_cls()
        result = runner.run(policy, seed=random.randint(0, 1_000_000))
        _save_run(result)
        line_fig, bar_fig = _build_figures(result)
        
        # Success status
        status_msg = f"✅ Simulation completed successfully! Policy: {policy_name}"
        return line_fig, bar_fig, status_msg
    
    except Exception as e:
        # Return error charts
        error_line = px.line()
        error_bar = px.bar()
        for fig in [error_line, error_bar]:
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#E7EBFF',
                title=f"Simulation Error: {str(e)}",
                title_font_color='#FF5B5B'
            )
        status_msg = f"❌ Error: {str(e)}"
        return error_line, error_bar, status_msg

if __name__ == "__main__":
    app.run(debug=True)
