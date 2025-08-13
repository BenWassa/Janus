Sprints by Week
Sprint 1 – Trait Glossary & Tagging API
Goal: Finalize trait names, concise definitions, example behaviors, and implement the in-engine tagging method.

Deliver: Trait glossary table (12 traits, each with definition + 2–3 example in-story triggers).

Deliver: Pseudocode or function spec for tag() and normalize() in the game engine.

Deliver: Dev HUD mockup showing live trait deltas.

Deep Context to provide with stock doc:

The working trait list above.

Rubric for weights.

Example of 2–3 fully tagged scene choices.

Engine’s current choice handling format.






Sprint 2 – Content Expansion: Act 1 (Mirrors)
Goal: Add micro/mid/pocket scenes + decoys to Act 1.

Deliver: +6 micro-scenes, +2 mid-stakes, +1 optional pocket scene.

Each choice tagged with {primary trait, primary weight, secondary trait, secondary weight}.

Ensure 30–40% decoy/no-weight choices.

Deep Context:

Current Act 1 script.

Desired tone (dreamlike, self-confrontational).

Examples of low vs high-weight decisions.

How to intersperse decoys to reduce “quiz” feel.








Sprint 3 – Content Expansion: Act 2 (Beasts)
Goal: As above, but for Act 2.

Deliver: +6 micro-scenes, +2 mid-stakes, +1 optional pocket.

Emphasis on moral tests, mercy vs cruelty.

Decoy ratio maintained.

Deep Context:

Current Act 2 script.

Trait mapping for aggression, control, compassion.

How Beasts represent externalized inner flaws.







Sprint 4 – Content Expansion: Act 3 (Whispers)
Goal: As above, but for Act 3.

Deliver: +6 micro-scenes, +2 mid-stakes, +1 optional pocket.

Decoys embedded.

Deep Context:

Current Act 3 script.

Trait mapping for secrecy, temptation, loyalty.















Sprint 5 – Midgame Payoffs
Goal: Author micro & mid-scene variations triggered by top trait(s).

Deliver: 20+ micro-payoffs (ambient lines, item descriptions, NPC remarks).

Deliver: 6–8 mid-scene forks keyed to top-1 or top-2 traits.

Format: if-trait templates ready to plug into engine.

Deep Context:

Example micro-payoffs from prototypes.

Mapping of traits to thematic payoff styles.

Rules for avoiding overt trait labeling.












Sprint 6 – Endgame Reveal Library
Goal: Create 9 end-reveal variants (3×3 primary/secondary trait grid).

Deliver: Narrative templates with variables for trait titles, metaphors, tone.

Deliver: Neutral fallback reveal for ties.

Ensure each reveal feels earned from cumulative play.

Deep Context:

Trait constellation logic.

Examples of good/bad reveals from playtest feedback.

Tone guidelines: reflective, poetic, non-preachy.













Sprint 7 – Engine Polish
Goal: Add save/load, HUD toggle, telemetry logging.

Deliver: CLI options, JSON save format, sample telemetry output.

Deliver: Minimal code changes for integration.

Maintain compatibility with tagging system.

Deep Context:

Current engine loop.

Desired HUD/CLI wireframe.

JSON save spec.













Sprint 8 – Playtest & Balancing
Goal: Tune weights, decoys, and payoff frequency.

Deliver: Recommended weight adjustments.

Deliver: Revised scenes or tags where balance is off.

Deliver: Playtest feedback synthesis.

Deep Context:

Test run logs with trait deltas.

Known exploits or over-strong traits.

Playtest survey results.





Sprint 9 - Repository Audit & Reorganization
Goal: Verify all content, code, and data assets are stored in the correct locations, consistently named, and match the project’s structural conventions. Move or rename as needed to meet the agreed organization scheme.

Stock Context
(Include same Stock Context Document from the commissioning doc so the AI knows the project scope & structure goals.)

Deep Context for Sprint 9
Target Structure:

bash
Copy
Edit
/src/           → All Python/engine code
/src/modules/   → Logical engine modules (tagging, payoffs, telemetry, etc.)
/data/          → Scenario scripts, trait libraries, payoff templates
/data/playtests → Logs, run summaries, feedback artifacts
/versions/      → Archived builds with date stamps
/docs/          → README.md, design docs, sprint reports
/tests/         → Automated or manual test scripts
Audit Steps:

Inventory: List every file + path in the repo.

Classify: For each file, determine if it’s:

Code (engine, modules, utilities)

Content (scenarios, templates, trait maps)

Documentation (design docs, reports, READMEs)

Test (scripts, fixtures)

Artifact (logs, telemetry, playtest outputs)

Verify Placement: Check that each file is in the correct directory per the structure above.

Relocate & Rename:

Move misplaced files into the right folder.

Apply consistent naming (snake_case for code, kebab-case or underscores for data files).

Dependency Check: Ensure moved code files still resolve imports correctly.

README Update: For any folder impacted, update its README to reflect current contents.

Report: Output before/after directory tree + list of changes.

Deliverables:

Updated directory tree snapshot (pre and post).

List of all moved/renamed files.

Confirmation that imports/build scripts run successfully after changes.

Updated READMEs in affected directories.





Sprint 10 – Scenario Depth + Decoys
Goal: Increase content density and camouflage to prevent testers from reverse-engineering the trait system.

Deliverables:

Add ~10 micro-scenes across all three Acts:

3 zero-weight decoys (purely narrative flavor)

3 low-weight (+0.2) plausible high-impact lookalikes

4 mid/high-weight choices (+0.5 / +0.8) filling coverage gaps

Review all existing scenes for “too obvious” weight–trait links.

Adjust wording or introduce alternate/decoy siblings to obscure mechanics.

Ensure major-weight choices never appear back-to-back in a single playthrough.

Deep Context:

Current Acts 1–3 scripts

Existing decoy placement map

List of “too obvious” traits and candidate adjustments















Sprint 11 – End-to-End Trait Reveal Pass
Goal: Guarantee that every playthrough produces a coherent, satisfying reveal with in-story callbacks.

Deliverables:

Verify the full trait-tracking loop (start → tag accumulation → top-3 determination → end reveal).

Fill gaps in the reveal library:

Every possible top-3 constellation must have a reveal

Provide a neutral fallback for ties

Ensure each Act has at least one payoff beat (micro or mid) triggered by the player’s current top trait(s).

Run 2–3 scripted playthrough simulations to confirm trait outcomes trigger correct reveals.

Deep Context:

Current reveal template library

Trait constellation mapping rules

Logs from simulated or past playthroughs














Sprint 12 – Alpha/Beta Test Setup
Goal: Deliver a playable, test-ready build for internal/external testers.

Deliverables:

Integrate save/load and telemetry logging:

Log choice ID, primary/secondary traits, and weight deltas

Add an internal debug HUD toggle showing:

Current trait totals

Last choice’s primary/secondary/weight

Package as a standalone build with simple run instructions.

Conduct 1–2 internal dry runs to validate stability and end-to-end flow before release to testers.

Deep Context:

Current engine code with save/load hooks

Telemetry output target format

OS/package dependencies and run instructions








Sprint 13: Testing Dashboard & Control Panel
Purpose
Create an interactive, cleanly‑styled dashboard that lets developers and testers adjust trait thresholds, run archetype or random simulations, and visually explore results. This will make it easy to fine‑tune the psychological weighting and see how archetype runs evolve across scenes and acts.

Stock Context (to attach with this sprint)
Use the same Stock Context Document from previous sprints (traits list, weight rubric, story structure, repo conventions).

Key constants restated:

Traits: Hubris, Avarice, Deception, Control & Perfectionism, Wrath, Fear & Insecurity, Impulsivity, Envy, Apathy & Sloth, Pessimism & Cynicism, Moodiness & Indirectness, Rigidity.

Weight categories: 0.0 (decoy), 0.2 (micro), 0.5 (mid), 0.8 (major).

End reveal logic: Top 3 traits after normalization.

Repo structure:

/src/ for all runtime and engine code

/data/ for scenario scripts, trait libraries, payoff templates, and test harness outputs (JSON)

/docs/ for design docs and sprint reports

Goal
Deliver a visual dashboard that:

Provides interactive controls (sliders, numeric inputs) for trait dominance thresholds, per‑trait caps, and decoy ratios.

Lets testers launch multiple runs (seeded random and archetype policies) directly from the interface.

Displays results with clear, attractive charts:

Line graphs tracking trait totals across decisions/acts for each run.

Grouped bar charts comparing final normalized trait scores across archetypes.

Optionally: separate deep‑dive charts per trait to compare archetypes.

Generates summary reports (tabular metrics, narrative summaries).

Uses our existing test harness under the hood (from Sprint 10–12) to execute runs and parse outputs.

Deliverables
1) Dashboard Application
Framework Choice: A Python web app using Plotly Dash (or similar), since it integrates with our Python codebase and can be served locally.

Directory Placement:

New module under /src/dashboard/ containing all Dash code.

Entry point script run_dashboard.py in /src/dashboard/ or a CLI hook in /src/cli/.

UI Layout:

Control Panel (top section):

Sliders/inputs for:

Dominance threshold (percentage of total normalized score required for a “clear” trait reveal).

Per‑trait act cap (soft cap slider).

Decoy ratio target.

Numeric fields for:

Number of random runs.

Random seed (optional; leave blank for auto‑generated).

Archetype selection (dropdown of preset policies).

Run buttons: “Run Random”, “Run Selected Archetype(s)”.

Visualization Area (middle section):

Primary Chart: line graph showing cumulative trait totals by decision step.

X‑axis: decision number (or scene index).

Y‑axis: trait total.

Lines: each trait (color-coded) or each archetype (choose one view or allow toggling).

Secondary Chart: grouped bar chart comparing final normalized scores across archetypes.

X‑axis: traits.

Y‑axis: normalized score (%).

Bars grouped by archetype, with legend.

Trait Deep‑Dive Tabs: optional tabbed area where selecting a trait displays a bar chart of that trait’s final scores across archetypes.

Summary Panel (bottom section):

A small table summarizing: run names, number of decisions, dominant/top‑3 traits, reveal narrative, pass/fail flags (for golden tests).

Option to download raw results as JSON or CSV.

Styling: Use a neutral, clean palette (greys, blues) consistent with Project Janus branding. Tooltips should explain controls and charts.

2) Backend Integration
Harness Calls: The dashboard must call the existing test harness (Runner API) to execute runs based on user input.

Result Parsing: After a run completes, the dashboard should parse trait progression and final normalized scores from harness outputs.

Threshold Application: When the tester adjusts dominance thresholds or caps, re-interpret run results accordingly (no need to rerun tests unless explicitly changed).

Error Handling: Display readable errors if harness execution fails or a run yields invalid results.

3) Data & Config
Data Source: Harness outputs should be read from /data/test_results/ if they already exist, or generated on demand into a temporary location (or into /data/test_results/ with unique names).

Config File: A YAML or JSON config under /data/dashboard_config.json to persist default threshold values, last used seed, or display preferences.

README: Document setup instructions in /docs/dashboard.md, including dependencies (pip install dash plotly) and run command (python src/dashboard/run_dashboard.py).

4) Visualization Components
Use Plotly (through Dash) for interactivity:

Line Graph: Use one trace per trait OR one trace per archetype (selectable).

Grouped Bar Chart: Use barmode "group" with traits on x-axis and archetypes on legend.

Trait Deep Dive: When a trait is selected, automatically regenerate a bar chart for that trait across archetypes.

5) Testing & Acceptance
Run a suite of archetype tests through the dashboard using existing HighWrath, HighControl, and decoy policies to confirm the graphs reflect expected trends.

Trigger random runs (e.g., 5 runs with different seeds) and verify charts update correctly.

Check that adjusting the dominance threshold changes the reveal classification live (e.g., from neutral to identifying a top trait).

Make sure UI elements disable while a run is executing and show progress to avoid confusion.

Deep Context for Sprint 13
The repository already contains /data/test_results.json formatted as an array of run objects with keys: decisions_made, trait_progression, final_traits, and final_reveal.

Use this format as the schema for new runs saved to /data/test_results/ — consistent keys for parsing.

The harness runner from previous sprints returns a similar structure.

Threshold and cap logic should be adjusted only at interpretation, not within the run — so the run data remains raw and can be reinterpreted without re-execution.

Keep all new code under /src/dashboard/ and avoid polluting core engine modules.

Acceptance Criteria
Runs Triggered via UI: Random and archetype runs can be launched, and results appear in charts without manual file movement.

Dynamic Thresholds: Adjusting thresholds instantly updates trait dominance and reveal classification for completed runs.

Charts & Tabs Functionality: All charts render correctly, switch views smoothly, and scale gracefully as runs are added.

Data Integrity: JSON results saved to /data/test_results/ remain intact; reloading the app displays saved runs.

Documentation: /docs/dashboard.md explains how to install dependencies, run the dashboard, and interpret the UI.




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
Goal: Implement bounded, auditable calibration and output a signed "best" config.

Deliverables:
- src/calibrator/config_schema.json – schema for policy multipliers and master guards.
- src/calibrator/calibrator.py – applies multipliers (0.8–2.0), anti-streak dampening, decay, scene caps, and ε-nudge.
- src/calibrator/optimizer.py – search with composite objective (balance↑ + policy deviation↓ + intent lock).
- configs/calibrator_v1.json – baseline knobs.
- snapshots/calibration_YYYYMMDD.json – winning config + KPIs + hash.
- tests/test_calibrator_bounds.py, tests/test_optimizer_objective.py.
- CLI: python -m src.calibrator.optimizer --in data/derived/runs_agg.csv --config configs/calibrator_v1.json --out snapshots/calibration_YYYYMMDD.json

Definition of Done
Composite score ≥ +15% vs baseline; major-streak <20%; tie margin >0.05; no single trait >35% (aggregate); snapshot written; tests pass.



