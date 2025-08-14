# Project Janus – Status Snapshot (2025-08-14)

## Overview
Project Janus is a retro-inspired text RPG where player choices both guide the story and quietly build a psychological profile, culminating in a personalized "Hero's Chronicle" of mind and myth.

## Version
- Current version: `v2.1-alpha`

## Repository Structure
- `/data/` – Structured game content (quests, characters, scenarios, psychological mappings).
- `/src/` – Engine entry point and reusable modules for tagging, save/load, telemetry, CLI helpers, dashboard, calibrator, and testing utilities.
- `/versions/` – Milestone implementations documenting project evolution.
- `/tests/` – Automated tests and fixtures for canonical flows, scoring logic, telemetry, and calibration.
- Additional directories support documentation, deployment, scripts, tools, configs, reports, and generated outputs.

## Testing
- `python -m pytest` → **17 passed**, 2 warnings (deprecated `datetime.utcnow`).

## Recent Activity
- `568cab1` – fix: update version to v2.1-alpha

## Sprint Progress
Sixteen sprints delivered:
1. Trait glossary and tagging API.
2. Act 1 "Mirrors" scenarios.
3. Act 2 "Beasts" scenarios.
4. Act 3 "Whispers" scenarios.
5. Midgame trait payoffs.
6. Endgame reveal library.
7. Save/load telemetry.
8. Trait balance from playtests.
9. Repository audit and reorganization.
10. Scenario depth and decoys.
11. End-to-end trait reveal pass.
12. Alpha/Beta test setup and packaging script.
13. Testing dashboard and control panel.
14. Data ingestion & analytics baseline.
15. Calibrator & optimization utilities.
16. Dashboard "Personality Mixer" with live slider readouts.

## Next Steps
- Gather feedback from alpha/beta testers.
- Expand scenario library and refine psychological mappings.
- Continue playtesting to validate trait balance.
- Iterate on the testing dashboard and integrate future codex features.
- Refine calibration workflow and analytics pipeline.
