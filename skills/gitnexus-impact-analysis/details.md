# Impact Analysis

Analyze what will break before making changes.

## Workflow

1. **Check index freshness**: `npx gitnexus status`
2. **Run impact analysis**: Use `gitnexus_impact({target: "X", direction: "upstream"})` to find dependents
3. **Review risks**: d=1 WILL BREAK, d=2 LIKELY AFFECTED, d=3 MAY NEED TESTING
4. **Check execution flows**: read_file affected process resources
5. **Pre-commit check**: `gitnexus_detect_changes()` to understand what your changes affect

## Risk Assessment

| Affected | Risk |
|----------|------|
| <5 symbols, few processes | LOW |
| 5-15 symbols, 2-5 processes | MEDIUM |
| >15 symbols or many processes | HIGH |
| Critical path (auth, payments) | CRITICAL |

## Commands

```bash
# Build/refresh the knowledge graph index
npx gitnexus analyze
# Check if index is stale
npx gitnexus status
# Delete stale index before re-index
npx gitnexus clean --force
```
