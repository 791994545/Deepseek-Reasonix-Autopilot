---
name: prototype
description: Build a throwaway prototype to refine a design before committing to real implementation. Two branches: terminal app (logic) or multi-variant UI.
---

# Prototype

Build a throwaway prototype to answer a specific question.

## Choose a branch

- Logic/state model feels wrong? → Build a terminal interactive app to test state machine
- UI look and feel uncertain? → Generate several distinct UI variants switchable via URL params

## Rules for both branches

1. Mark code as PROTOTYPE clearly from day one
2. Single command to run
3. Default to no persistence (state in memory)
4. No polish - no tests, no error handling beyond keeping it runnable
5. Surface state after every operation
6. Delete or absorb when done - only keep the answer
