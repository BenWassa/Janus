# Changelog — pilot_humility_hubris

## Unreleased

### Removed
- Removed decorative constellation canvas and related CSS/JS (frontend cleanup). Rationale: unused/experimental background effect; removal reduces complexity and eliminates fragile runtime behavior.

### Fixes
- Fixed a critical JS bug that could reassign the global `document` object and added defensive DOM guards and a startup integrity check. This improves stability when the UI is trimmed or embedded.

### Verification
- Project unit tests run locally and pass after the changes.

(Generated automatically by repo maintenance script.)
