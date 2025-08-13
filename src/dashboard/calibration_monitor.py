"""
Dash layout and callbacks for the interactive calibration monitor.

This module provides the full UI and state management for the "Personality Mixer"
and its associated master controls. It is designed to be embedded within the main
dashboard application.
"""

from dash import dcc, html, Input, Output, State, ALL
from dash.exceptions import PreventUpdate

# Define the policy channels for the mixer UI.
# The 'key' corresponds to the trait names used in the simulation's config.
POLICY_CHANNELS = [
    ("Hubris", "Hubris"),
    ("Control", "Control"),
    ("Fear", "Fear"),
    ("Deception", "Deception"),
    ("Avarice", "Avarice"),
    ("Wrath", "Wrath"),
    ("Envy", "Envy"),
    ("Rigidity", "Rigidity"),
]

def _policy_strip(label: str, key: str) -> html.Div:
    """Creates the UI elements for a single policy fader channel."""
    slider_id = {"type": "fader", "index": key}
    readout_id = {"type": "readout", "index": key}
    return html.Div([
        html.Label(label, htmlFor=str(slider_id), className="policy-label"),
        dcc.Slider(
            id=slider_id, min=0.8, max=2.0, step=0.05, value=1.0,
            marks=None, className="policy-fader", tooltip={"placement": "bottom", "always_visible": False}
        ),
        html.Div("1.00", id=readout_id, className="policy-readout"),
    ], className="policy-strip")

# Define the main layout for the calibration monitor
layout = html.Div([
    html.Div([
        # Left side: Mixer channels for personality traits
        html.Div([
            html.H3("Personality Mixer", className="mixer-title"),
            html.P("Adjust real-time policy multipliers to tune AI behavior. These settings will be used for the next simulation run.", className="mixer-description"),
            html.Div(
                [_policy_strip(label, key) for label, key in POLICY_CHANNELS],
                className="mixer-channels",
            ),
        ], className="mixer-panel"),

        # Right side: Master controls for global parameters
        html.Div([
            html.H3("Master Controls", className="master-title"),
            html.P("Fine-tune global simulation parameters that affect decision-making logic.", className="master-description"),
            html.Div([
                html.Div([
                    html.Label("Decay Factor", htmlFor="decay-slider", className="master-label"),
                    dcc.Slider(id="decay-slider", min=0.0, max=0.1, value=0.03, step=0.01, marks=None, tooltip={"placement": "bottom"}),
                    html.Div("0.03", id="decay-readout", className="master-readout"),
                ], className="master-control-group"),
                html.Div([
                    html.Label("Anti-Streak Dampening", htmlFor="anti-streak-slider", className="master-label"),
                    dcc.Slider(id="anti-streak-slider", min=0.0, max=0.3, value=0.15, step=0.01, marks=None, tooltip={"placement": "bottom"}),
                    html.Div("0.15", id="anti-streak-readout", className="master-readout"),
                ], className="master-control-group"),
                 html.Div([
                    html.Label("Epsilon (Randomness %)", htmlFor="epsilon-slider", className="master-label"),
                    dcc.Slider(id="epsilon-slider", min=0.0, max=0.1, value=0.03, step=0.01, marks=None, tooltip={"placement": "bottom"}),
                    html.Div("3.0%", id="epsilon-readout", className="master-readout"),
                ], className="master-control-group"),
            ], className="master-controls"),

            html.H3("Status", className="status-title"),
            html.Div([
                html.Span("Configuration Ready", className="status-chip"),
            ], className="status-chips"),

        ], className="master-panel"),
    ], className="calibration-monitor-content"),
    # This dcc.Store is the critical component that holds the live state of the mixer
    dcc.Store(id='calibration-config-store', data={})
])

def register_callbacks(app):
    """Register all callbacks for the calibration monitor to make it interactive."""

    # Create a list of all inputs for the central store callback
    store_inputs = [
        Input({"type": "fader", "index": ALL}, "value"),
        Input("decay-slider", "value"),
        Input("anti-streak-slider", "value"),
        Input("epsilon-slider", "value"),
    ]
    # Corresponding state to get the keys for the faders
    store_state = State({"type": "fader", "index": ALL}, "id")

    # This single callback aggregates all calibration settings into the dcc.Store
    @app.callback(
        Output('calibration-config-store', 'data'),
        store_inputs,
        store_state,
        prevent_initial_call=True
    )
    def update_calibration_store(fader_values, decay, anti_streak, epsilon, fader_ids):
        """On any control change, update the central config store."""
        if not fader_values:
            raise PreventUpdate

        multipliers = {fader_id['index']: value for fader_id, value in zip(fader_ids, fader_values)}

        # This dictionary is the configuration that will be passed to the simulation runner
        config = {
            "multipliers": multipliers,
            "decay": decay,
            "anti_streak": anti_streak,
            "epsilon": epsilon,
            # Add other necessary config keys with default values
            "scene_cap": 0.5,
            "act_cap": 1.5,
        }
        return config

    # Update individual slider readouts to provide immediate visual feedback
    for _, key in POLICY_CHANNELS:
        @app.callback(
            Output({"type": "readout", "index": key}, "children"),
            Input({"type": "fader", "index": key}, "value"),
            prevent_initial_call=True
        )
        def update_fader_readout(value):
            return f"{value:.2f}"

    # Callbacks for master control readouts
    @app.callback(Output("decay-readout", "children"), Input("decay-slider", "value"), prevent_initial_call=True)
    def update_decay_readout(v): return f"{v:.2f}"

    @app.callback(Output("anti-streak-readout", "children"), Input("anti-streak-slider", "value"), prevent_initial_call=True)
    def update_antistreak_readout(v): return f"{v:.2f}"

    @app.callback(Output("epsilon-readout", "children"), Input("epsilon-slider", "value"), prevent_initial_call=True)
    def update_epsilon_readout(v): return f"{v*100:.1f}%"