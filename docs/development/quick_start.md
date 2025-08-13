# Janus RPG - Development Setup

## Quick Start

1. **Choose your development approach:**
   - Start prototyping in `versions/v0-experiments/experiments/`
   - Work on a specific version in `versions/`
   - Develop shared components in `src/`

2. **For prototyping (recommended first step):**
   ```bash
   cd versions/v0-experiments/experiments
   python experiment_main.py
   ```

3. **Project structure at a glance:**
   ```
   src/           # Shared, reusable components
   versions/      # Version-specific implementations (includes experiments)
   data/          # Game content (JSON files)
   tests/         # Testing suite
   deployment/    # Production builds
   docs/          # Documentation
   ```

## Development Workflow

### Phase 1: Prototyping
- Work in `versions/v0-experiments/experiments/`
- Test concepts quickly
- Validate psychological assessment ideas

### Phase 2: Core Development
- Build reusable components in `src/`
- Focus on modularity and clean architecture
- Comprehensive testing

### Phase 3: Version Implementation
- Create version-specific features in `versions/`
- Use shared components from `src/`
- Version-specific content and mechanics

### Phase 4: Deployment
- Build stable releases in `deployment/`
- Comprehensive testing and validation
- Release packaging

## Key Design Principles

### Modular Architecture
- Separate game logic from psychology assessment
- Data-driven content system
- Clean separation between versions

### Psychology Integration
- Covert assessment through gameplay
- Ethical and transparent approach
- Scientifically grounded trait analysis

### User Experience
- Engaging narrative-driven gameplay
- Meaningful choices with consequences
- Personalized "Hero's Chronicle" output

## Next Steps

1. **Start prototyping**: Run the experiment in `versions/v0-experiments/experiments/experiment_main.py`
2. **Design your first quest**: Create content in `data/quests/`
3. **Implement core systems**: Build game engine components in `src/modules/`
4. **Add psychological assessment**: Develop profiling algorithms in `src/modules/`

## Documentation

- [Project Structure](../technical/project_structure.md) - Detailed architecture overview
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Development guidelines and ethics
- [Docs Overview](../README.md) - Comprehensive documentation
- Each module has its own README with specific guidance

Ready to build something amazing! 🎮🧠
