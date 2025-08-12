# Project Janus - Structure Overview

## 🏗️ Project Architecture

This repository follows a modular, version-controlled structure designed for iterative development of the psychological RPG game.

## 📁 Directory Structure

```
Janus/
├── src/                        # Core source code (shared across versions)
│   ├── core/                   # Core game engine components
│   ├── game/                   # Game mechanics and logic
│   ├── psychology/             # Psychological profiling system
│   └── utils/                  # Utility functions and helpers
│
├── versions/                   # Version-specific implementations
│   ├── v1-prototype/           # Initial prototype version
│   ├── v2-alpha/              # Alpha release version
│   └── v3-beta/               # Beta release version
│
├── prototype/                  # Experimental and testing area
│   ├── experiments/            # Feature experiments and POCs
│   └── tests/                  # Prototype-specific tests
│
├── deployment/                 # Production deployment files
│   ├── build/                  # Build artifacts
│   └── release/                # Release packages
│
├── data/                       # Game content and data
│   ├── quests/                 # Quest definitions and storylines
│   ├── characters/             # Character data and NPCs
│   └── scenarios/              # Psychological scenarios
│
├── tests/                      # Comprehensive testing suite
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
│
└── docs/                       # Documentation
```

## 🔄 Development Workflow

### 1. Prototyping Phase
- Work in `prototype/experiments/` for new features
- Use `prototype/tests/` for experimental testing
- Validate concepts before moving to versioned development

### 2. Version Development
- Each version in `versions/` represents a milestone
- Import shared components from `src/`
- Version-specific features go in respective version directories

### 3. Production Deployment
- Stable releases are built in `deployment/build/`
- Final packages stored in `deployment/release/`

## 🧠 Core Components

### Psychology Module (`src/psychology/`)
- Personality trait scoring (Big Five, etc.)
- Decision analysis algorithms
- Profile generation system

### Game Engine (`src/core/`)
- Text rendering and input handling
- Save/load system
- Game state management

### Game Logic (`src/game/`)
- Quest system
- Character interactions
- Narrative branching

## 📊 Data Organization

Game content is separated from code in the `data/` directory:
- **Quests**: Story content, choices, and outcomes
- **Characters**: NPC definitions and dialogue trees
- **Scenarios**: Psychological testing scenarios

## 🚀 Getting Started

1. Start prototyping in `prototype/experiments/`
2. Move stable features to `src/` for reuse
3. Create version-specific implementations in `versions/`
4. Test thoroughly using both `prototype/tests/` and `tests/`
5. Deploy stable versions through `deployment/`

## 🔧 Best Practices

- Keep shared code in `src/` modular and well-documented
- Use semantic versioning for version directories
- Document all psychological algorithms and scoring methods
- Maintain clear separation between game logic and content data
- Test psychological profiling accuracy and ethical implications
