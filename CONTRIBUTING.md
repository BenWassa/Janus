# Contributing to Project Janus

## Development Workflow

### 1. Setting Up Development Environment
```bash
# Clone the repository
git clone <repository-url>
cd Janus

# Set up your preferred development environment
# (Python, Node.js, or your chosen language)
```

### 2. Prototyping New Features
- Start in `prototype/experiments/`
- Create focused, small experiments
- Document your findings
- Test concepts thoroughly

### 3. Implementing Features
- Move proven concepts to appropriate `src/` modules
- Follow existing code structure and patterns
- Update documentation
- Add comprehensive tests

### 4. Version Development
- Work in appropriate version directory (`versions/`)
- Use shared components from `src/`
- Maintain version-specific documentation
- Test integration thoroughly

## Code Guidelines

### General Principles
- **Modularity**: Keep components focused and reusable
- **Documentation**: Document all psychological algorithms
- **Ethics**: Consider privacy and consent implications
- **Testing**: Validate both functionality and psychological accuracy

### Psychology Module Guidelines
- Document all trait calculations
- Cite psychological research where applicable
- Implement ethical safeguards
- Validate assessment accuracy

### Game Module Guidelines
- Separate content from logic
- Make systems data-driven
- Consider replayability
- Balance engagement with assessment

## Testing Requirements

### Before Submitting
1. Run all unit tests
2. Validate psychological assessments
3. Test user experience flow
4. Check ethical considerations

### Psychological Validation
- Verify trait calculations
- Test for bias and fairness
- Validate against established research
- Consider cultural sensitivity

## Pull Request Process

1. Create feature branch from main
2. Implement changes following guidelines
3. Add/update tests and documentation
4. Submit pull request with clear description
5. Address review feedback

## Ethical Considerations

### Required for All Contributors
- Respect user privacy
- Implement transparent data practices
- Consider psychological impact
- Follow research ethics guidelines

### Psychological Assessment Ethics
- Inform users about profiling
- Provide opt-out mechanisms
- Avoid harmful stereotyping
- Maintain assessment validity
