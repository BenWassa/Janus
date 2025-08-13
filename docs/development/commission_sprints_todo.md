Sprint 14 — Data Ingestion & Analytics Baseline
Purpose
Create a single, canonical dataset from all runs and produce baseline calibration KPIs.

Scope & Deliverables

Canonical Trait Map (resolve duplicates):

“Control & Perfectionism”→Control; “Apathy & Sloth”→Apathy; “Pessimism & Cynicism”/“Cynicism”→Cynicism; “Moodiness & Indirectness”→Moodiness.

Code

src/analytics/canonical.py – mapping + validators (raise on non-canonical).

src/analytics/ingest_runs.py – load & normalize all data/test_results/run_*.json (support both dashboard and CLI run schemas).

src/analytics/baseline_metrics.py – KPIs: entropy, policy-bias heatmap, scene pressure, major-streaks, tie margins, dominance curves.

Artifacts

data/derived/runs_agg.csv (long format: run, policy, step, scene_id, choice_id, primary/secondary, pw/sw, delta, totals, final_normalized, top3).

reports/baseline_metrics.md (numbers only).

Tests

tests/test_canonical.py (no duplicate/non-canonical traits).

tests/test_ingest_schema.py (schema coverage; spot-check parity with source).

CLI

python -m src.analytics.ingest_runs --runs-dir data/test_results --out data/derived/runs_agg.csv

python -m src.analytics.baseline_metrics --in data/derived/runs_agg.csv --report reports/baseline_metrics.md

Definition of Done

All runs load; zero non-canonical traits; runs_agg.csv count ≥ sum of decisions across runs; baseline KPIs rendered; tests pass.














Sprint 15 — Calibrator & Optimization
Purpose
Implement bounded, auditable calibration and output a signed “best” config.

Scope & Deliverables

Code

src/calibrator/config_schema.json – schema for policy multipliers and master guards.

src/calibrator/calibrator.py – applies: multipliers (0.8–2.0), anti-streak (~15% dampen next 2 same-trait decisions after double-major), decay (λ≤0.03 per-step or 0.95 per-act), scene caps (0.5 per scene; 1.5 per act, tapered), ε-nudge (0–0.03 near-ties only).

src/calibrator/optimizer.py – grid/Bayesian search with composite objective: balance↑ + policy deviation↓ + intent lock (each policy’s signature trait remains Top-2).

Configs & Artifacts

configs/calibrator_v1.json – baseline knobs.

snapshots/calibration_YYYYMMDD.json – winning config + KPIs + hash.

Tests

tests/test_calibrator_bounds.py, tests/test_optimizer_objective.py.

CLI

python -m src.calibrator.optimizer --in data/derived/runs_agg.csv --config configs/calibrator_v1.json --out snapshots/calibration_YYYYMMDD.json

Definition of Done

Composite score ≥ +15% vs baseline; major-streak <20%; tie margin >0.05; no single trait >35% (aggregate); snapshot written; tests pass.















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