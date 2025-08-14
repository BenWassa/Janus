# Prototype v1 - Labyrinth RPG Pilot

This is the first working prototype of Project Janus - a console-based RPG that subtly profiles player psychology through narrative choices.

## What It Is
**"Labyrinth of Three Doors"** - A single-file Python game that presents players with a mysterious labyrinth containing three paths (Mirrors, Beasts, Whispers), each designed to reveal different aspects of personality through player choices.

## Features Implemented
- **Rich Console Interface**: Beautiful text-based UI using the Rich library with panels, tables, and color formatting
- **Personality Tracking**: Three core traits (Bravery, Cunning, Chaos) that evolve based on player decisions
- **Branching Narrative**: Multiple paths through the labyrinth with 6 different endings
- **Inventory System**: Items that affect both gameplay and personality assessment
- **Atmospheric Design**: Dynamic environment descriptions with wind patterns and ambient details
- **Choice-Driven Psychology**: Each decision subtly reveals player preferences and personality traits

## Game Structure
The pilot features three main paths:
1. **Door of Mirrors** - Tests self-reflection and identity choices
2. **Door of Beasts** - Explores courage and relationship with nature/authority
3. **Door of Whispers** - Examines honesty, patience, and trust

Each path leads to different endings: Heroic, Tragic, Absurd, Mysterious, Comedic, or Bittersweet.

## Technical Requirements
- Python 3.10+
- Rich library (`pip install rich`)

## Usage
```
python labyrinth_rpg_pilot.py
```

## Psychological Assessment
The prototype tracks personality through:
- **Bravery**: Willingness to face danger or unknown situations
- **Cunning**: Strategic thinking and careful observation
- **Chaos**: Embrace of unpredictability and unconventional choices

Player choices organically adjust these traits, creating a psychological profile through natural gameplay.

## Development Status
✅ **WORKING PROTOTYPE** - Fully playable from start to finish
- Core narrative complete with all paths and endings
- Personality tracking functional
- UI polished and user-friendly
- Ready for playtesting and feedback

## Next Steps
- Gather player feedback on narrative effectiveness
- Analyze correlation between choices and personality assessment
- Refine psychological profiling accuracy
- Prepare for v2 expansion with additional scenarios
