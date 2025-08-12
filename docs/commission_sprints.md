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
Goal: Increase density and camouflage so the trait system isn’t transparent to testers.

Deliverables:

Add ~10 micro-scenes spread evenly across Acts 1–3.

At least 3 zero-weight decoys purely for flavor.

At least 3 low-weight (+0.2) choices that could plausibly be major.

Remaining 4 balanced across +0.5 or +0.8 where missing coverage.

Review all existing choice weightings for “obviousness.”

If a choice reads as clearly linked to a trait, soften via alternate wording or add decoy siblings.

Ensure pacing: major-weight choices never appear back-to-back.

Deep Context to provide:

Current scenario scripts (Acts 1–3).

List of existing decoys and their placement.

Known “too obvious” choice examples.









Sprint 11 – End-to-End Trait Reveal Pass
Goal: Ensure every possible run produces a coherent, satisfying endgame payoff.

Deliverables:

Verify trait tracking loop works start → finish.

Fill any gaps in reveal library — every top-3 constellation (or fallback grouping) must have a narrative template.

Ensure at least one micro/mid payoff triggers in each Act for most playstyles.

Run a 2–3 simulated playthroughs (scripted inputs) to verify different trait outcomes produce the correct reveals.

Deep Context to provide:

Current trait payoff library.

Trait constellation mapping (top-3 logic).

Example playthrough logs from Sprint 9.










Sprint 12 – Alpha/Beta Test Setup
Goal: Package the game for real-world playtesting.

Deliverables:

Integrate save/load and basic telemetry logging (choice IDs, traits before/after).

Add lightweight debug HUD toggle for internal testers showing:

Current trait scores

Last choice’s primary/secondary/weight

Package as a standalone, easy-to-run build with instructions.

Run 1–2 internal dry runs to confirm stability before handing to external testers.

Deep Context to provide:

Current engine code and save/load hooks.

Example telemetry output format.

Packaging requirements (target OS, dependencies, run instructions).