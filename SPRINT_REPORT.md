# Project Janus – Sprint Report

## Overview
This document summarizes the work completed across thirteen development sprints and the current state of the Project Janus repository.

## Sprint Accomplishments
1. **Sprint 1 – Trait glossary and tagging API.** Introduced psychological weighting for quest choices, enabling traits to be tracked throughout gameplay.
2. **Sprint 2 – Act 1 "Mirrors" scenarios.** Added reflective scenarios with trait-tagged choices.
3. **Sprint 3 – Act 2 "Beasts" scenarios.** Implemented moral trials featuring bestial reflections of player flaws.
4. **Sprint 4 – Act 3 "Whispers" scenarios.** Delivered temptation-focused scenes exploring secrets and loyalty.
5. **Sprint 5 – Midgame trait payoffs.** Created micro payoff events that trigger based on trait ranks.
6. **Sprint 6 – Endgame reveal library.** Added narrative templates that summarize dominant and secondary traits.
7. **Sprint 7 – Save/load telemetry.** Integrated lightweight event logging and command-line options for save and load.
8. **Sprint 8 – Trait balance from playtests.** Balanced trait progression using feedback and logs from playtest runs.
9. **Sprint 9 – Repository audit and reorganization.** Consolidated directories and verified imports and documentation.
10. **Sprint 10 – Scenario depth and decoys.** Added micro-scenes, decoy encounters, and high-weight options to obscure trait linkage.
11. **Sprint 11 – End-to-end trait reveal pass.** Verified the full trait-tracking loop and ensured reveal coverage for all trait constellations.
12. **Sprint 12 – Alpha/Beta test setup.** Introduced last-choice HUD details, expanded telemetry logging, and added a packaging script for tester builds.
13. **Sprint 13 – Testing dashboard and control panel.** Delivered a Dash-powered dashboard for running archetype simulations and visualising trait progression.

## Repository Status
- Source code and data are organized under clearly defined directories (`src/`, `data/`, `versions/`, etc.).
- Readme files in each module describe usage and integration points and have been reviewed for accuracy.
- Playtest artifacts and trait payoff libraries are stored under `data/` for iterative tuning.

## Next Steps
- Gather feedback from alpha/beta testers.
- Expand scenario library and refine psychological mappings.
- Continue playtesting to validate trait balance.
- Iterate on the testing dashboard and integrate future codex features.
