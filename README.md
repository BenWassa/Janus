# Project Janus
A retro-inspired text RPG where your story shapes — and secretly reveals — your psychological profile. Decisions guide the plot and quietly measure traits like openness, risk tolerance, and attachment style, culminating in a personalized "Hero'\''s Chronicle" of mind and myth.

## Project Overview
Project Janus blends the charm of a classic text-based fantasy adventure with the intrigue of hidden psychological profiling. Every choice you make — in quests, dialogues, and moral dilemmas — subtly shapes your journey and reveals the inner contours of your character.

At the end of your quest, you receive your Hero'\''s Chronicle:
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
Core system implementation divided into specialized modules:

#### `/src/core/` - Game Engine
Fundamental components including the main game loop, rendering system, input handling, and state management. [See core README](src/core/README.md) for architecture details.

#### `/src/game/` - Game Logic
RPG-specific mechanics, quest systems, character interactions, and narrative flow management. [See game README](src/game/README.md) for gameplay implementation.

#### `/src/psychology/` - Profiling System
Covert psychological assessment engine that analyzes player decisions and generates personality profiles. [See psychology README](src/psychology/README.md) for assessment methodologies.

#### `/src/utils/` - Utilities
Shared helper functions, configuration management, and common tools used across the project. [See utils README](src/utils/README.md) for available utilities.

### 📁 `/versions/` - Development Iterations
Version-specific implementations showing project evolution:

#### `/versions/v1-prototype/` - Working Pilot
Complete playable "Labyrinth of Three Doors" prototype demonstrating core concepts. [See v1 README](versions/v1-prototype/README.md) for pilot details.

#### `/versions/v2-alpha/` - Enhanced Version
Expanded feature set with improved psychology engine and additional content. [See v2 README](versions/v2-alpha/README.md) for alpha features.

#### `/versions/v3-beta/` - Production Candidate
Feature-complete beta with polished UI, comprehensive testing, and deployment readiness. [See v3 README](versions/v3-beta/README.md) for beta status.

### 📁 `/prototype/` - Experimental Development
Research and experimentation space for testing new concepts, algorithms, and game mechanics before integration into main versions. [See prototype README](prototype/README.md) for experimental features.

### 📁 `/tests/` - Quality Assurance
Comprehensive testing suite including unit tests for individual components and integration tests for system-wide functionality. [See tests README](tests/README.md) for testing procedures.

### 📁 `/docs/` - Documentation
Complete project documentation including game design documents, technical guides, psychology methodologies, and user manuals. [See docs README](docs/README.md) for documentation structure.

### 📁 `/deployment/` - Release Management
Production deployment configuration, build processes, and release management tools for distributing the game across multiple platforms. [See deployment README](deployment/README.md) for release procedures.

## Getting Started

1. **Play the Prototype**: Try the v1 pilot in `/versions/v1-prototype/` to experience the core concept
2. **Explore the Code**: Review `/src/` modules to understand the architecture
3. **Read the Docs**: Check `/docs/` for comprehensive design and technical documentation
4. **Run Tests**: Execute test suites in `/tests/` to verify system functionality

## Vision
Future versions may expand into adaptive NPC behavior, multiplayer "party dynamics" profiling, and ethically designed research modules for psychological studies.

## Development Principles
- **Ethical Psychology**: Transparent, opt-in profiling with clear privacy protections
- **Modular Design**: Easy extension and modification of game content and mechanics
- **Player-Centric**: Engaging gameplay that naturally reveals personality traits
- **Research-Ready**: Robust data collection and analysis capabilities for academic use'