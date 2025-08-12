# Deployment

Production deployment configuration and release management.

## Build Process
1. Run comprehensive tests
2. Bundle version-specific code
3. Include necessary data files
4. Create distribution packages

### Alpha/Beta Build

Use the helper script to bundle a tester-ready archive:

```
python deployment/build_alpha.py
```

The script outputs `dist/janus_alpha.zip` containing `src/` and `data/`. Testers can unzip it and run the engine:

```
python src/engine.py --telemetry log.json
```

## Release Management
- Semantic versioning
- Release notes generation
- Distribution packaging
- Update mechanisms

## Platforms
- Standalone executable
- Web deployment
- Package distribution
