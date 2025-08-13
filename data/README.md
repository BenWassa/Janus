# Game Data

This directory contains all game content separated from code for easy modification and localization.

## Structure

### Quests (`quests/`)
JSON files defining quest structures, dialogue, choices, and outcomes.

### Characters (`characters/`)
NPC definitions, personality traits, and dialogue trees.

### Scenarios (`scenarios/`)
Psychological testing scenarios and their scoring parameters. Includes decoy scenes and varied weighting to camouflage trait tracking.


### Payoffs (`payoffs/`)
Trait-driven micro payoffs, mid-scene forks, and endgame reveal templates keyed to player profiles.

Includes:
- `midgame.json` – micro payoffs and mid-scene forks keyed to traits.
- `endgame_reveals.json` – 3×3 trait grid of endgame reveal templates with neutral fallback.

### Playtests (`playtests/`)
Logs and survey results from playtest sessions used for calibration and user studies.

### Derived (`derived/`)
Aggregated run metrics and processed outputs generated from gameplay sessions.

### Samples (`samples/`)
Example save files and telemetry logs for reference and testing.

### Test Results (`test_results/`)
JSON outputs from automated test runs and batch simulations.

### Dashboard Config (`dashboard_config.json`)
Default configuration file for the developer dashboard.


## Format Guidelines
- Use JSON for structured data
- Include metadata for content management
- Maintain consistent naming conventions
- Document psychological assessment mapping

## Content Creation
1. Define psychological objectives first
2. Create engaging narrative content
3. Map choices to personality traits
4. Test for bias and accuracy
