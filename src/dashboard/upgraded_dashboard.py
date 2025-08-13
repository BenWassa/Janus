import json
import subprocess
import sys
import os
from datetime import datetime

# Ensure required packages are installed
def install_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_path])

install_requirements()
import random
from pathlib import Path
from typing import Dict, Any

from dash import Dash, dcc, html, Input, Output, State, callback_context
import plotly.express as px
import plotly.graph_objects as go

# Ensure repository root is on path so we can import testing modules
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from testing import runner
from testing.policies import random_policy, hubris_forward, control_fear

DATA_DIR = ROOT / "data" / "test_results"

POLICIES = {
    "Seeded Random": {
        "class": random_policy.SeededRandomPolicy,
        "description": "Makes random decisions for unpredictable gameplay",
        "icon": "🎲"
    },
    "Hubris Forward": {
        "class": hubris_forward.HubrisForwardPolicy,
        "description": "Aggressive strategy focusing on bold moves",
        "icon": "⚡"
    },
    "Control & Fear": {
        "class": control_fear.ControlFearPolicy,
        "description": "Cautious approach emphasizing control",
        "icon": "🛡️"
    },
}

def get_initial_charts():
    """Create initial empty charts with modern styling."""
    empty_line = go.Figure()
    empty_line.add_annotation(
        text="Click 'Run Simulation' to generate trait progression",
        xref="paper", yref="paper",
        x=0.5, y=0.5, xanchor='center', yanchor='middle',
        font=dict(size=16, color='#64748B'),
        showarrow=False
    )
    
    empty_bar = go.Figure()
    empty_bar.add_annotation(
        text="Waiting for simulation results...",
        xref="paper", yref="paper",
        x=0.5, y=0.5, xanchor='center', yanchor='middle',
        font=dict(size=16, color='#64748B'),
        showarrow=False
    )
    
    # Apply consistent dark theme
    for fig in [empty_line, empty_bar]:
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0',
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40),
            height=400
        )
        fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
    
    return empty_line, empty_bar

def create_policy_card(policy_name, policy_info, is_selected=False):
    """Create a modern policy selection card."""
    border_color = "#3B82F6" if is_selected else "rgba(255,255,255,0.1)"
    bg_color = "rgba(59,130,246,0.1)" if is_selected else "#1E293B"
    
    return html.Div([
        html.Div([
            html.Div(policy_info["icon"], className="policy-icon"),
            html.H3(policy_name, className="policy-name"),
            html.P(policy_info["description"], className="policy-description")
        ], className="policy-content"),
        html.Div("✓" if is_selected else "", className="policy-checkmark")
    ], 
    className="policy-card",
    style={
        "border": f"2px solid {border_color}",
        "backgroundColor": bg_color,
    },
    id={"type": "policy-card", "index": policy_name})

def create_metric_card(title, value, subtitle="", trend=None):
    """Create a metric display card."""
    trend_color = "#10B981" if trend == "up" else "#EF4444" if trend == "down" else "#64748B"
    trend_icon = "↗" if trend == "up" else "↘" if trend == "down" else ""
    
    return html.Div([
        html.H4(title, className="metric-title"),
        html.Div([
            html.Span(str(value), className="metric-value"),
            html.Span(f" {trend_icon}", style={"color": trend_color}) if trend_icon else None
        ], className="metric-value-container"),
        html.P(subtitle, className="metric-subtitle") if subtitle else None
    ], className="metric-card")

app = Dash(__name__)

# Enhanced layout with modern design
app.layout = html.Div([
    # Header Section
    html.Div([
        html.Div([
            html.H1([
                html.Span("🚪", className="header-icon"),
                "Janus Testing Dashboard"
            ], className="main-title"),
            html.P("Advanced AI behavior testing and analysis platform", 
                   className="subtitle")
        ], className="header-content"),
        
        # Quick Stats Row
        html.Div([
            html.Div(id="quick-stats", children=[
                create_metric_card("Simulations Run", "0", "Total tests completed"),
                create_metric_card("Avg Decision Time", "—", "Processing speed"),
                create_metric_card("Success Rate", "—", "Completion percentage"),
                create_metric_card("Last Run", "Never", "Most recent test")
            ])
        ], className="stats-grid")
    ], className="dashboard-header"),
    
    # Main Content Area
    html.Div([
        # Left Panel - Controls
        html.Div([
            html.Div([
                html.H2("🎮 Policy Selection", className="section-title"),
                html.P("Choose an AI strategy for behavior testing", 
                       className="section-description"),
                
                # Policy Cards Grid
                html.Div([
                    create_policy_card(name, info, name == "Seeded Random") 
                    for name, info in POLICIES.items()
                ], className="policy-grid", id="policy-selection"),
                
                # Advanced Settings
                html.Div([
                    html.H3("⚙️ Advanced Settings", className="subsection-title"),
                    html.Div([
                        html.Label("Random Seed:", className="input-label"),
                        dcc.Input(
                            id="seed-input",
                            type="number",
                            placeholder="Leave empty for random",
                            className="modern-input"
                        )
                    ], className="input-group"),
                    html.Div([
                        html.Label("Max Steps:", className="input-label"),
                        dcc.Slider(
                            id="max-steps",
                            min=10, max=1000, value=100, step=10,
                            marks={i: str(i) for i in range(0, 1001, 200)},
                            className="modern-slider"
                        )
                    ], className="input-group")
                ], className="advanced-settings"),
                
                # Action Button
                html.Div([
                    html.Button([
                        html.Span("▶", className="button-icon"),
                        "Run Simulation"
                    ], id="run-btn", n_clicks=0, className="primary-button"),
                    html.Button([
                        html.Span("📊", className="button-icon"),
                        "View History"
                    ], id="history-btn", n_clicks=0, className="secondary-button")
                ], className="action-buttons")
            ], className="control-panel")
        ], className="left-panel"),
        
        # Right Panel - Results
        html.Div([
            # Status Banner
            html.Div(id="status-banner", className="status-banner hidden"),
            
            # Charts Section
            html.Div([
                html.H2("📈 Real-time Analysis", className="section-title"),
                
                # Chart Tabs
                dcc.Tabs(id="chart-tabs", value="progression", 
                        className="custom-tabs", children=[
                    dcc.Tab(label="Trait Progression", value="progression", 
                           className="custom-tab"),
                    dcc.Tab(label="Final Scores", value="final", 
                           className="custom-tab"),
                    dcc.Tab(label="Decision Tree", value="decisions", 
                           className="custom-tab")
                ]),
                
                # Chart Content
                html.Div(id="chart-content", children=[
                    dcc.Graph(id="main-chart", 
                             figure=get_initial_charts()[0],
                             className="main-chart",
                             config={'displayModeBar': False})
                ])
            ], className="charts-section"),
            
            # Results Summary
            html.Div([
                html.H3("🎯 Results Summary", className="subsection-title"),
                html.Div(id="results-summary", className="results-grid")
            ], className="summary-section")
        ], className="right-panel")
    ], className="main-content"),
    
    # Hidden data stores
    dcc.Store(id="selected-policy", data="Seeded Random"),
    dcc.Store(id="simulation-data", data={}),
    dcc.Store(id="simulation-history", data=[])
], className="app-container")

def _save_run(result: Dict[str, Any], policy_name: str) -> None:
    """Save run result with enhanced metadata."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(DATA_DIR.glob("run_*.json"))
    fname = DATA_DIR / f"run_{len(existing) + 1}.json"
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "policy": policy_name,
        "decisions_made": sum(1 for e in result["trace"] if not e.get("end")),
        "trait_progression": result["trace"],
        "final_traits": result["final"]["normalized"],
        "final_reveal": result["final"].get("top3", []),
        "metadata": {
            "total_steps": len(result["trace"]),
            "completion_status": "success" if result.get("final") else "incomplete"
        }
    }
    
    with fname.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    
    return data

def create_enhanced_line_chart(result: Dict[str, Any]):
    """Create an enhanced line chart with modern styling."""
    line_rows = []
    for entry in result["trace"]:
        if entry.get("end"):
            continue
        step = entry["step"]
        for trait, total in entry["totals"].items():
            line_rows.append({"step": step, "trait": trait, "total": total})
    
    if not line_rows:
        return get_initial_charts()[0]
    
    # Create figure with custom colors
    fig = px.line(line_rows, x="step", y="total", color="trait",
                  title="Trait Evolution Over Time")
    
    # Enhanced styling
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family="Inter"),
        title=dict(
            text="Trait Evolution Over Time",
            font=dict(size=20, color='#F1F5F9'),
            x=0.5, xanchor='center'
        ),
        legend=dict(
            bgcolor='rgba(30,41,59,0.8)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(color='#E2E8F0')
        ),
        hovermode='x unified',
        margin=dict(l=60, r=60, t=80, b=60),
        height=500
    )
    
    fig.update_xaxes(
        gridcolor='rgba(255,255,255,0.1)',
        title_font=dict(color='#CBD5E1'),
        tickfont=dict(color='#94A3B8')
    )
    fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.1)',
        title_font=dict(color='#CBD5E1'),
        tickfont=dict(color='#94A3B8')
    )
    
    # Custom color palette
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
    for i, trace in enumerate(fig.data):
        trace.line.color = colors[i % len(colors)]
        trace.line.width = 3
    
    return fig

def create_enhanced_bar_chart(result: Dict[str, Any]):
    """Create an enhanced bar chart for final scores."""
    final = result.get("final", {}).get("normalized", {})
    
    if not final:
        return get_initial_charts()[1]
    
    # Sort by values for better visualization
    sorted_traits = sorted(final.items(), key=lambda x: x[1], reverse=True)
    traits, values = zip(*sorted_traits)
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(traits), 
            y=list(values),
            marker=dict(
                color=values,
                colorscale='Viridis',
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            text=[f'{v:.2f}' for v in values],
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        )
    ])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family="Inter"),
        title=dict(
            text="Final Trait Distribution",
            font=dict(size=20, color='#F1F5F9'),
            x=0.5, xanchor='center'
        ),
        xaxis_title="Traits",
        yaxis_title="Normalized Score",
        margin=dict(l=60, r=60, t=80, b=60),
        height=500
    )
    
    fig.update_xaxes(
        gridcolor='rgba(255,255,255,0.1)',
        title_font=dict(color='#CBD5E1'),
        tickfont=dict(color='#94A3B8')
    )
    fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.1)',
        title_font=dict(color='#CBD5E1'),
        tickfont=dict(color='#94A3B8')
    )
    
    return fig

# Callback for policy selection
@app.callback(
    [Output("selected-policy", "data"),
     Output("policy-selection", "children")],
    [Input({"type": "policy-card", "index": ALL}, "n_clicks")],
    prevent_initial_call=True
)
def update_policy_selection(n_clicks):
    if not any(n_clicks):
        raise PreventUpdate
    
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    clicked_policy = ctx.triggered[0]["prop_id"].split(".")[0]
    policy_name = eval(clicked_policy)["index"]
    
    # Rebuild policy cards with new selection
    new_cards = [
        create_policy_card(name, info, name == policy_name) 
        for name, info in POLICIES.items()
    ]
    
    return policy_name, new_cards

# Main simulation callback
@app.callback(
    [Output("main-chart", "figure"),
     Output("status-banner", "children"),
     Output("status-banner", "className"),
     Output("simulation-data", "data"),
     Output("results-summary", "children"),
     Output("quick-stats", "children")],
    Input("run-btn", "n_clicks"),
    [State("selected-policy", "data"),
     State("seed-input", "value"),
     State("simulation-history", "data")],
    prevent_initial_call=True,
)
def run_simulation(n_clicks, policy_name, seed_value, history):
    if not n_clicks:
        raise PreventUpdate
    
    try:
        # Validate policy
        if not policy_name or policy_name not in POLICIES:
            raise ValueError(f"Invalid policy: {policy_name}")
        
        # Set up policy and seed
        policy_cls = POLICIES[policy_name]["class"]
        policy = policy_cls()
        seed = seed_value if seed_value is not None else random.randint(0, 1_000_000)
        
        # Run simulation
        result = runner.run(policy, seed=seed)
        
        # Save results
        saved_data = _save_run(result, policy_name)
        
        # Update history
        history.append(saved_data)
        
        # Create enhanced charts
        line_fig = create_enhanced_line_chart(result)
        
        # Success status banner
        status_content = html.Div([
            html.Span("✅", className="status-icon"),
            html.Span(f"Simulation completed successfully! Policy: {policy_name}", 
                     className="status-text"),
            html.Span(f"Seed: {seed}", className="status-detail")
        ])
        status_class = "status-banner success-banner"
        
        # Results summary
        final_traits = result.get("final", {}).get("normalized", {})
        decisions_made = sum(1 for e in result["trace"] if not e.get("end"))
        
        summary_cards = [
            create_metric_card("Decisions Made", decisions_made, "Total choices"),
            create_metric_card("Final Traits", len(final_traits), "Measured attributes"),
            create_metric_card("Top Trait", max(final_traits.keys(), key=final_traits.get) if final_traits else "None", "Highest scoring"),
            create_metric_card("Simulation Seed", seed, "Reproducibility key")
        ]
        
        # Updated quick stats
        avg_decisions = sum(len(h.get("trait_progression", [])) for h in history) / len(history) if history else 0
        quick_stats = [
            create_metric_card("Simulations Run", len(history), "Total tests completed", "up"),
            create_metric_card("Avg Decisions", f"{avg_decisions:.1f}", "Per simulation"),
            create_metric_card("Success Rate", "100%", "Completion rate", "up"),
            create_metric_card("Last Run", datetime.now().strftime("%H:%M"), "Just completed")
        ]
        
        return line_fig, status_content, status_class, result, summary_cards, quick_stats
        
    except Exception as e:
        # Error handling
        error_fig = get_initial_charts()[0]
        error_fig.add_annotation(
            text=f"Simulation Error: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color='#EF4444'),
            showarrow=False
        )
        
        status_content = html.Div([
            html.Span("❌", className="status-icon"),
            html.Span(f"Error: {str(e)}", className="status-text")
        ])
        status_class = "status-banner error-banner"
        
        return error_fig, status_content, status_class, {}, [], []

# Chart tab switching callback
@app.callback(
    Output("chart-content", "children"),
    [Input("chart-tabs", "value"),
     Input("simulation-data", "data")],
    prevent_initial_call=True
)
def update_chart_content(active_tab, simulation_data):
    if not simulation_data:
        return [dcc.Graph(id="main-chart", figure=get_initial_charts()[0], 
                         className="main-chart", config={'displayModeBar': False})]
    
    if active_tab == "progression":
        fig = create_enhanced_line_chart(simulation_data)
    elif active_tab == "final":
        fig = create_enhanced_bar_chart(simulation_data)
    else:  # decisions
        # Placeholder for decision tree visualization
        fig = get_initial_charts()[0]
        fig.add_annotation(
            text="Decision Tree Visualization Coming Soon",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color='#64748B'),
            showarrow=False
        )
    
    return [dcc.Graph(id="main-chart", figure=fig, 
                     className="main-chart", config={'displayModeBar': False})]

if __name__ == "__main__":
    app.run(debug=True)
