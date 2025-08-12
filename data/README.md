# Game Data

This directory contains all game content separated from code for easy modification and localization.

## Structure

### Quests (`quests/`)
JSON files defining quest structures, dialogue, choices, and outcomes.

### Characters (`characters/`)
NPC definitions, personality traits, and dialogue trees.

### Scenarios (`scenarios/`)
Psychological testing scenarios and their scoring parameters.


### Payoffs (`payoffs/`)
Trait-driven micro payoffs, mid-scene forks, and endgame reveal templates keyed to player profiles.

Includes:
- `midgame.json` – micro payoffs and mid-scene forks keyed to traits.
- `endgame_reveals.json` – 3×3 trait grid of endgame reveal templates with neutral fallback.


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
