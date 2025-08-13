Sprint 16 — Dashboard “Personality Mixer” (Calibration Monitor)
Purpose
Deliver a mixer-style calibration UX: faders for policy multipliers (trait channels) and master bus (decay, anti-streak, caps, ε). Minimal by default; details on hover/click.

Scope & Deliverables

Code

Add src/dashboard/calibration_monitor.py and import into the app (or extend run_dashboard.py).

Tabs: Policies (Hubris, Control-Fear, Deception-Avarice, Reckless, Balanced, Random), Master Bus.

Policy channel strips: fader 0.8–2.0 + numeric readout, Mute (sets 1.0), Solo (impact preview), Meter (expected contribution shift using cached aggregates).

Master controls: Decay slider, Anti-streak toggle + intensity, Caps inputs, ε slider.

Status chips: Entropy, Max Policy Deviation, Major-Streak Rate, Tie Margin.

Hover “?” → one-line plain-English explain; Click → compact panel (2–3 bullets + micro sparkline).

Actions: Apply (recompute on cached runs), Snapshot (config + metrics), Reset (baseline), Export CSV (aggregates).

Guardrails: soft-stops on faders; badges (green/amber/red) with hover rationale.

Accessibility: keyboardable sliders/toggles; ARIA labels; tooltips on focus.

Implementation Notes

Reuse Sprint-14 aggregates and Sprint-15 calibrator; do not re-simulate the engine.

Keep UI collapsed by default; reveal details only on hover/click.

Provide what_if_state store; on Apply, show Before/After overlays and flash diff chips.

Definition of Done

Mixer renders; Apply/Snapshot/Reset/Export work; chips update; guardrail badges present; minimal-until-hover behavior; accessibility checks pass.