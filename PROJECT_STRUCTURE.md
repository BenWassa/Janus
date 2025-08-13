# Project Janus - Structure Overview

## 🏗️ Project Architecture

This repository follows a modular, version-controlled structure designed for iterative development of the psychological RPG game.

## 📁 Directory Structure

```
Janus/
├── src/                        # Core source code
│   ├── engine.py               # Main game loop
│   └── modules/                # Reusable engine modules (tagging, telemetry, save system)
├── versions/                   # Version-specific implementations
│   ├── v0-experiments/         # Research and prototype experiments
│   ├── v1-prototype/           # Initial prototype version
│   ├── v2-alpha/               # Alpha release version
│   └── v3-beta/                # Beta release version
├── deployment/                 # Production deployment files
├── data/                       # Game content and data
│   ├── quests/                 # Quest definitions and storylines
│   ├── characters/             # Character data and NPCs
│   ├── scenarios/              # Psychological scenarios
│   ├── payoffs/                # Trait payoff templates
│   ├── playtests/              # Logs and feedback artifacts
│   ├── derived/                # Aggregated run metrics
│   ├── samples/                # Example save and telemetry files
│   └── test_results/           # Outputs from automated test runs
├── tests/                      # Testing scripts
└── docs/                       # Documentation
```

## 🔄 Development Workflow

### 1. Prototyping Phase
- Work in `versions/v0-experiments/experiments/` for new features
- Validate concepts before moving to versioned development

### 2. Version Development
- Each version in `versions/` represents a milestone
- Import shared components from `src/`
- Version-specific features go in respective version directories

### 3. Production Deployment
- Stable releases are built in `deployment/`
- Final packages stored for distribution

## 🧠 Core Components

### Engine (`src/engine.py`)
- Command-line game loop
- Save/load handling
- Telemetry integration

### Modules (`src/modules/`)
- Trait tagging utilities
- Save system helpers
- Telemetry logging

## 📊 Data Organization

Game content is separated from code in the `data/` directory:
- **Quests**: Story content, choices, and outcomes
- **Characters**: NPC definitions and dialogue trees
- **Scenarios**: Psychological testing scenarios
- **Payoffs**: Trait-based payoff templates
- **Playtests**: Logs and survey results
- **Derived**: Aggregated run metrics
- **Samples**: Example save and telemetry files
- **Test Results**: JSON outputs from automated test runs

## 🚀 Getting Started

1. Start prototyping in `versions/v0-experiments/`
2. Move stable features to `src/` for reuse
3. Create version-specific implementations in `versions/`
4. Test thoroughly using `tests/`
5. Deploy stable versions through `deployment/`

## 🔧 Best Practices

- Keep shared code in `src/` modular and well-documented
- Use semantic versioning for version directories
- Document all psychological algorithms and scoring methods
- Maintain clear separation between game logic and content data
- Test psychological profiling accuracy and ethical implications
