"""Dash layout for the calibration monitor.

This module provides a minimal skeleton for the "Personality Mixer" UX
specified in Commission Sprint 16. It exposes a `layout` object that can
be embedded in the dashboard and a `register_callbacks` helper for slider
readouts. The implementation focuses on structure rather than the full
interactive behaviour described in the sprint brief.
"""

from dash import dcc, html
from dash.dependencies import Input, Output

# Policy channels included in the mixer. Each channel exposes a slider that
# ranges from 0.8 to 2.0 along with a numeric readout. The sprint brief also
# mentions mute/solo/meter controls; these are represented here as placeholders
# so that the UI can evolve without breaking the import contract.
POLICY_CHANNELS = [
    ("Hubris", "hubris"),
    ("Control-Fear", "control_fear"),
    ("Deception-Avarice", "deception_avarice"),
    ("Reckless", "reckless"),
    ("Balanced", "balanced"),
    ("Random", "random"),
]


def _policy_strip(label: str, key: str) -> html.Div:
    """Create the UI elements for a single policy channel."""
    return html.Div(
        [
            html.Label(label, htmlFor=f"fader-{key}"),
            dcc.Slider(
                id=f"fader-{key}",
                min=0.8,
                max=2.0,
                step=0.1,
                value=1.0,
                marks=None,
                className="policy-fader",
            ),
            html.Div("1.0", id=f"readout-{key}", className="policy-readout"),
        ],
        className="policy-strip",
    )


# Build the calibration monitor layout. Master controls are represented with
# basic Dash components; they provide hooks for future enhancements while
# keeping the current implementation lightweight.
layout = html.Div(
    [
        html.H2("Personality Mixer", className="mixer-title"),
        html.Div(
            [_policy_strip(label, key) for label, key in POLICY_CHANNELS],
            className="mixer-channels",
        ),
        html.H3("Master Controls", className="master-title"),
        html.Div(
            [
                html.Label("Decay", htmlFor="decay-slider"),
                dcc.Slider(
                    id="decay-slider", min=0.0, max=1.0, value=0.5, step=0.01
                ),
                html.Label("Anti-streak", htmlFor="anti-streak-toggle"),
                dcc.Checklist(
                    id="anti-streak-toggle",
                    options=[{"label": "Enable", "value": "on"}],
                    value=[],
                ),
                html.Label("Anti-streak Intensity", htmlFor="anti-streak-intensity"),
                dcc.Slider(
                    id="anti-streak-intensity", min=0.0, max=1.0, value=0.0, step=0.1
                ),
                html.Label("Caps", htmlFor="caps-input"),
                dcc.Input(id="caps-input", type="number", value=0),
                html.Label("ε", htmlFor="epsilon-slider"),
                dcc.Slider(
                    id="epsilon-slider", min=0.0, max=1.0, value=0.05, step=0.01
                ),
            ],
            className="master-controls",
        ),
        html.H3("Status", className="status-title"),
        html.Div(
            [
                html.Span("Entropy: —", className="status-chip"),
                html.Span("Max Policy Deviation: —", className="status-chip"),
                html.Span("Major-Streak Rate: —", className="status-chip"),
                html.Span("Tie Margin: —", className="status-chip"),
            ],
            className="status-chips",
        ),
        html.Div(
            [
                html.Button("Apply", id="apply-button"),
                html.Button("Snapshot", id="snapshot-button"),
                html.Button("Reset", id="reset-button"),
                html.Button("Export CSV", id="export-button"),
            ],
            className="action-buttons",
        ),
    ],
    className="calibration-monitor",
)


def register_callbacks(app) -> None:
    """Register simple readout callbacks for each policy slider.

    This keeps the UI responsive without implementing the full calibration
    logic. Each callback updates the numeric readout next to its slider.
    """

    for _, key in POLICY_CHANNELS:
        @app.callback(
            Output(f"readout-{key}", "children"), 
            Input(f"fader-{key}", "value"),
            prevent_initial_call=True
        )
        def update_readout(value, key=key):
            if value is None:
                return "1.0"
            return f"{value:.2f}"
