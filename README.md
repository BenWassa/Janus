# Project Janus
A retro-inspired text RPG where your story shapes — and secretly reveals — your psychological profile. Decisions guide the plot and quietly measure traits like openness, risk tolerance, and attachment style, culminating in a personalized "Hero's Chronicle" of mind and myth.

**Current Version:** `v2-alpha` (see [`VERSION`](VERSION)).

For an overview of all milestone builds, see [`versions/README.md`](versions/README.md).

## Project Overview
Project Janus blends the charm of a classic text-based fantasy adventure with the intrigue of hidden psychological profiling. Every choice you make — in quests, dialogues, and moral dilemmas — subtly shapes your journey and reveals the inner contours of your character.

At the end of your quest, you receive your Hero's Chronicle:
- A narrative recap of your adventures
- An inferred profile across traits like the Big Five, risk tolerance, attachment style, and more
- Insights into how your decisions reflected (or defied) your underlying tendencies

## Core Features
- Branching narrative with multiple endings
- Covert psychological scoring system
- Replayable scenarios with different personality outcomes
- Modular design for adding new quests, dilemmas, and scoring frameworks

## Project Structure

### 📁 `/data/` - Game Content
Structured game data separated from code for easy modification and localization. Contains quests, characters, scenarios, and their psychological assessment mappings. [See data README](data/README.md) for content creation guidelines.

### 📁 `/src/` - Source Code
Engine entry point and reusable modules.
- `engine.py` – main game loop
- `modules/` – trait tagging, save system, telemetry utilities

### 📁 `/versions/` - Development Iterations
Version-specific implementations showing project evolution. See [`versions/README.md`](versions/README.md) for details on each milestone.

### 📁 `/tests/` - Quality Assurance
Testing scripts and fixtures. [See tests README](tests/README.md) for procedures.

### 📁 `/docs/` - Documentation
Complete project documentation including design notes, technical guides, and psychology references. [See docs README](docs/README.md) for structure.

### 📁 `/deployment/` - Release Management
Production deployment configuration, build processes, and release management tools. Use `deployment/build_alpha.py` to bundle a tester-ready archive. [See deployment README](deployment/README.md) for details.

## Getting Started
1. **Run the Alpha Build**
   ```bash
   python deployment/build_alpha.py
   unzip dist/janus_v2-alpha.zip
   python dist/janus_v2-alpha/src/engine.py --telemetry log.json
   ```
2. **Play the Prototype**: Try the v1 pilot in `/versions/v1-prototype/` to experience the core concept.
3. **Explore the Code**: Review `/src/` modules to understand the architecture.
4. **Read the Docs**: Check `/docs/` for comprehensive design and technical documentation.
5. **Run Tests**: Execute test scripts in `/tests/` to verify system functionality.

## Vision
Future versions may expand into adaptive NPC behavior, multiplayer "party dynamics" profiling, and ethically designed research modules for psychological studies.

## Development Principles
- **Ethical Psychology**: Transparent, opt-in profiling with clear privacy protections
- **Modular Design**: Easy extension and modification of game content and mechanics
- **Player-Centric**: Engaging gameplay that naturally reveals personality traits
- **Research-Ready**: Robust data collection and analysis capabilities for academic use
