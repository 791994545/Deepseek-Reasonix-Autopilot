# Diagnose - Systematic Debugging

A rigorous debugging loop.

## Steps

1. **Reproduce** - Create reliable reproduction steps
2. **Minimize** - Strip non-essentials to isolate root cause
3. **Hypothesize** - Form specific hypothesis
4. **Instrument** - Add logging/tests to validate
5. **Fix** - Apply minimal fix
6. **Regression** - Verify no other behavior changed

## Rules

- Never guess a fix without instrumenting first
- Change one variable at a time
- Document what was learned
