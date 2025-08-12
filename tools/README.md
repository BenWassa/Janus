# Tools Directory

Development and testing tools for Project Janus.

## Files

### `test_harness.py`
Automated testing harness for validating psychological profiling system.
- Runs predefined decision sequences
- Reports trait progression and final outcomes
- Validates choice-to-trait mappings
- Tests decoy effectiveness

**Usage:**
```bash
cd tools
python test_harness.py
```

Results are saved to `../outputs/test_results.json`

## Development Workflow

1. Use test harness to validate changes
2. Run before/after major content updates
3. Verify psychological accuracy of new scenarios
4. Test trait balancing and reveal system
