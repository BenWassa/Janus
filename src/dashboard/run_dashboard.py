import json
import subprocess
import sys
import os
from datetime import datetime

# Ensure required packages are installed
def install_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        print("🔄 Installing dashboard dependencies...")
        # Install silently
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_path],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Dependencies installed successfully")

install_requirements()
import random
from pathlib import Path
from typing import Dict, Any

from dash import Dash, dcc, html, Input, Output, State, callback_context, ALL
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go

# Ensure repository root is on path so we can import testing modules
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from testing import runner
from testing.policies import (
    random_policy, hubris_forward, control_fear,
    deception_avarice, reckless_chaotic, balanced_human
)

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
    "Deception & Avarice": {
        "class": deception_avarice.DeceptionAvaricePolicy,
        "description": "Seeks profit and advantage through cunning",
        "icon": "🐍"
    },
    "Reckless Chaotic": {
        "class": reckless_chaotic.RecklessChaoticPolicy,
        "description": "Impulsive, high variance decision maker",
        "icon": "🌪️"
    },
    "Balanced Human": {
        "class": balanced_human.BalancedHumanPolicy,
        "description": "Moderate choices with occasional inconsistencies",
        "icon": "⚖️"
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
            html.Div([
                html.H3(policy_name, className="policy-name"),
                html.P(policy_info["description"], className="policy-description")
            ], className="policy-text-content")
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

app = Dash(external_stylesheets=['/assets/dashboard.css'])
app.title = "Janus Dashboard"

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
                create_metric_card("Avg Decisions", "—", "Per simulation"),
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
                        className="custom-tabs-container", children=[
                    dcc.Tab(label="Trait Progression", value="progression",
                           className="custom-tab", selected_className="custom-tab--selected"),
                    dcc.Tab(label="Final Scores", value="final",
                           className="custom-tab", selected_className="custom-tab--selected"),
                    dcc.Tab(label="Decision Flow", value="decisions",
                           className="custom-tab", selected_className="custom-tab--selected")
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
        "trace": result["trace"],
        "final": result["final"],
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
    trait_series = {}
    for entry in result["trace"]:
        if entry.get("end"): continue
        step = entry.get("step")
        for trait, total in entry.get("totals", {}).items():
            trait_series.setdefault(trait, []).append((step, total))

    if not trait_series: return get_initial_charts()[0]

    trait_final_totals = {t: s[-1][1] for t, s in trait_series.items() if s}
    sorted_traits = sorted(trait_final_totals, key=trait_final_totals.get, reverse=True)

    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
    fig = go.Figure()
    for i, trait in enumerate(sorted_traits):
        series = trait_series.get(trait, [])
        steps, totals = zip(*series) if series else ([], [])
        fig.add_trace(go.Scatter(
            x=steps, y=totals, mode='lines', name=trait,
            line=dict(color=colors[i % len(colors)], width=3)
        ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family="Inter"),
        title=dict(text="<b>Trait Evolution Over Time</b>", font=dict(size=20), x=0.5),
        legend=dict(bgcolor='rgba(30,41,59,0.8)', bordercolor='rgba(255,255,255,0.1)', font=dict(color='#E2E8F0')),
        hovermode='x unified', margin=dict(l=60, r=60, t=80, b=60), height=500,
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='#CBD5E1')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='#CBD5E1'))
    )
    return fig

import textwrap # Make sure to have this import at the top of your file

def create_decision_tree_chart(result: Dict[str, Any]):
    """
    Create an enhanced, ascending decision flow timeline with automatic text wrapping
    to prevent horizontal collision.
    """
    trace = result.get("trace", [])
    decisions = [entry for entry in trace if not entry.get("end")]
    decisions.sort(key=lambda d: d.get('step', 0))

    if not decisions:
        fig = go.Figure()
        fig.add_annotation(text="No decision data available.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    TRAIT_COLORS = {
        'Control': '#3B82F6', 'Fear': '#F59E0B', 'Deception': '#10B981', 'Hubris': '#EF4444',
        'Envy': '#8B5CF6', 'Avarice': '#EC4899', 'Rigidity': '#64748B', 'Cynicism': '#A1A1AA',
        'Wrath': '#DC2626', 'Apathy & Sloth': '#78716C', 'Impulsivity': '#F97316',
        'Pessimism & Cynicism': '#A1A1AA', 'Moodiness & Indirectness': '#D946EF', 'default': '#94A3B8'
    }
    
    # --- KEY FIX: Helper function to wrap long text for HTML display ---
    def wrap_text(text, width=45):
        """Wraps text to a specified width and joins with <br> for HTML."""
        return '<br>'.join(textwrap.wrap(text, width=width))
    # ----------------------------------------------------------------

    fig = go.Figure()
    num_steps = len(decisions)
    spacing_multiplier = 1.5
    y_positions = [-i * spacing_multiplier for i in range(num_steps)]

    fig.add_trace(go.Scatter(
        x=[0] * num_steps, y=y_positions,
        mode='lines', line=dict(color='rgba(148, 163, 184, 0.3)', width=1.5), hoverinfo='none'
    ))

    for i, d in enumerate(decisions):
        y_pos = y_positions[i]
        primary_trait = d.get('primary', 'None')
        color = TRAIT_COLORS.get(primary_trait, TRAIT_COLORS['default'])

        fig.add_trace(go.Scatter(
            x=[0], y=[y_pos], mode='markers',
            marker=dict(size=14, color=color, line=dict(width=2, color='rgba(255, 255, 255, 0.2)')),
            hoverinfo='none', showlegend=False
        ))
        
        fig.add_annotation(
            x=-1.2, y=y_pos, text=f"<b>#{d.get('step', i+1)}</b>",
            xref="x", yref="y", showarrow=False, align="right", xanchor="right", font=dict(color="#94A3B8", size=12)
        )
        
        fig.add_annotation(
            x=-0.1, y=y_pos, text=f"<b>{d['scene_id']}</b>",
            xref="x", yref="y", showarrow=False, align="right", xanchor="right", font=dict(color="#CBD5E1", size=12)
        )

        # --- USE THE WRAPPED TEXT ---
        choice_text_wrapped = wrap_text(d['text'])
        fig.add_annotation(
            x=0.1, y=y_pos + 0.2, text=choice_text_wrapped,
            xref="x", yref="y", showarrow=False, align="left", xanchor="left", font=dict(color="#F1F5F9", size=13)
        )
        # ---------------------------

        delta_val = d.get('delta', {}).get(primary_trait, 0.0)
        impact_text = f"<b>{delta_val:+.1f} {primary_trait}</b>" if delta_val != 0 else "<i>No trait change</i>"
        fig.add_annotation(
            x=0.1, y=y_pos - 0.25, text=impact_text,
            xref="x", yref="y", showarrow=False, align="left", xanchor="left", font=dict(color=color, size=12)
        )

        totals = d.get('totals', {})
        if totals:
            sorted_totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:3]
            top3_text = "<br>".join([f"<span style='color:{TRAIT_COLORS.get(k, TRAIT_COLORS['default'])}'>●</span> {k}: {v:.1f}" for k, v in sorted_totals])
            fig.add_annotation(
                x=1.5, y=y_pos, text=top3_text, # Pushed further right for more space
                xref="x", yref="y", showarrow=False, align="right", xanchor="right",
                font=dict(color="#94A3B8", size=11),
                bordercolor="rgba(148, 163, 184, 0.2)", borderwidth=1, borderpad=6, bgcolor="rgba(30, 41, 59, 0.6)"
            )

    fig.update_layout(
        title=dict(text="<b>Decision Flow & Trait Impact</b>", font=dict(size=20, color='#F1F5F9'), x=0.5),
        showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, range=[-1.4, 1.7]), # Expanded range to fit the moved box
        yaxis=dict(visible=False, range=[y_positions[-1] - spacing_multiplier, y_positions[0] + spacing_multiplier]),
        margin=dict(l=40, r=40, t=80, b=20),
        height=max(600, num_steps * 100)
    )
    return fig

def create_enhanced_bar_chart(result: Dict[str, Any]):
    """Create an enhanced bar chart for final scores."""
    final = result.get("final", {}).get("normalized", {})
    if not final: return get_initial_charts()[1]

    sorted_traits = sorted(final.items(), key=lambda x: x[1], reverse=True)
    traits, values = zip(*sorted_traits)
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#64748B']

    fig = go.Figure(data=[go.Bar(x=list(traits), y=list(values), text=[f'{v:.1f}' for v in values], textposition='auto', marker_color=[colors[i%len(colors)] for i in range(len(traits))])])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0', family="Inter"),
        title=dict(text="<b>Final Trait Distribution</b>", font=dict(size=20), x=0.5),
        xaxis_title="Traits", yaxis_title="Normalized Score",
        margin=dict(l=60, r=60, t=80, b=60), height=500,
        xaxis=dict(categoryorder='total descending', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

# Callback for policy selection
@app.callback(
    [Output("selected-policy", "data"), Output("policy-selection", "children")],
    [Input({"type": "policy-card", "index": ALL}, "n_clicks")],
    prevent_initial_call=True
)
def update_policy_selection(n_clicks):
    if not any(n_clicks): raise PreventUpdate
    ctx = callback_context
    if not ctx.triggered: raise PreventUpdate

    clicked_policy_id = ctx.triggered[0]["prop_id"].split(".")[0]
    policy_name = json.loads(clicked_policy_id)["index"]

    new_cards = [create_policy_card(name, info, name == policy_name) for name, info in POLICIES.items()]
    return policy_name, new_cards

# Main simulation callback
@app.callback(
    [Output("main-chart", "figure"), Output("status-banner", "children"), Output("status-banner", "className"),
     Output("simulation-data", "data"), Output("results-summary", "children"), Output("quick-stats", "children")],
    Input("run-btn", "n_clicks"),
    [State("selected-policy", "data"), State("seed-input", "value"), State("simulation-history", "data"), State("chart-tabs", "value")],
    prevent_initial_call=True,
)
def run_simulation(n_clicks, policy_name, seed_value, history, active_tab):
    if not n_clicks: raise PreventUpdate

    try:
        if not policy_name or policy_name not in POLICIES: raise ValueError(f"Invalid policy: {policy_name}")
        policy_cls = POLICIES[policy_name]["class"]
        seed = seed_value if seed_value is not None else random.randint(0, 1_000_000)

        result = runner.run(policy_cls(), seed=seed)
        saved_data = _save_run(result, policy_name)
        history = (history or []) + [saved_data]

        # Display the correct chart based on the currently active tab
        if active_tab == 'progression': fig = create_enhanced_line_chart(result)
        elif active_tab == 'final': fig = create_enhanced_bar_chart(result)
        elif active_tab == 'decisions': fig = create_decision_tree_chart(result)
        else: fig = create_enhanced_line_chart(result) # Default case

        status_content = html.Div([html.Span("✅", className="status-icon"), html.Span(f"Simulation completed! Policy: {policy_name}", className="status-text"), html.Span(f"Seed: {seed}", className="status-detail")])
        status_class = "status-banner success-banner"

        final_traits = result.get("final", {}).get("normalized", {})
        decisions_made = sum(1 for e in result["trace"] if not e.get("end"))

        summary_cards = [
            create_metric_card("Decisions Made", decisions_made, "Total choices"),
            create_metric_card("Dominant Trait", max(final_traits, key=final_traits.get, default="N/A"), f"Score: {max(final_traits.values(), default=0):.1f}"),
            create_metric_card("Simulation Seed", seed, "For reproducibility"),
            create_metric_card("Final Traits", len(final_traits), "Measured attributes")
        ]

        avg_decisions = sum(h["decisions_made"] for h in history) / len(history) if history else 0
        quick_stats = [
            create_metric_card("Simulations Run", len(history), "Total tests completed", "up"),
            create_metric_card("Avg Decisions", f"{avg_decisions:.1f}", "Per simulation"),
            create_metric_card("Success Rate", "100%", "Completion rate"),
            create_metric_card("Last Run", datetime.now().strftime("%H:%M:%S"), "Just now")
        ]

        return fig, status_content, status_class, result, summary_cards, quick_stats

    except Exception as e:
        error_fig = get_initial_charts()[0]
        error_fig.add_annotation(text=f"Simulation Error: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, font=dict(size=16, color='#EF4444'), showarrow=False)
        status_content = html.Div([html.Span("❌", className="status-icon"), html.Span(f"Error: {str(e)}", className="status-text")])
        status_class = "status-banner error-banner"
        return error_fig, status_content, status_class, {}, [], []

# Chart tab switching callback
@app.callback(
    Output("chart-content", "children"),
    [Input("chart-tabs", "value"), Input("simulation-data", "data")],
    prevent_initial_call=True
)
def update_chart_content(active_tab, simulation_data):
    if not simulation_data:
        return [dcc.Graph(id="main-chart", figure=get_initial_charts()[0], className="main-chart", config={'displayModeBar': False})]

    if active_tab == "progression": fig = create_enhanced_line_chart(simulation_data)
    elif active_tab == "final": fig = create_enhanced_bar_chart(simulation_data)
    elif active_tab == "decisions": fig = create_decision_tree_chart(simulation_data)
    else: fig = get_initial_charts()[0]

    return [dcc.Graph(id="main-chart", figure=fig, className="main-chart", config={'displayModeBar': False})]

if __name__ == "__main__":
    import webbrowser, threading, time
    print("\n" + "="*60 + "\n🚀 JANUS DASHBOARD STARTING\n" + "="*60)
    print("📊 Initializing interactive dashboard...")
    def open_browser():
        time.sleep(2)
        print("\n🌐 Opening dashboard in your browser...")
        webbrowser.open('http://127.0.0.1:8050/')

    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    print("🎯 Dashboard URL: http://127.0.0.1:8050/")
    print("="*60)

    try:
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Thanks for using Janus!\n" + "="*60)