---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace — ensures an isolated workspace exists via native tools or git worktree fallback
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace. Use for feature branches that need clean separation.

**Core principle**: Detect existing isolation first → use native tools → fall back to git. Never fight the harness.

**Announce at start**: "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Step 0: Detect Existing Isolation

**Before creating anything, check if you are already in an isolated workspace.**

```bash
git rev-parse --git-dir
git rev-parse --git-common-dir
git branch --show-current
```

If `GIT_DIR != GIT_COMMON_DIR` (and not a submodule): You are already in a linked worktree. Skip to setup.

If `GIT_DIR == GIT_COMMON_DIR` (or in a submodule): You are in a normal repo checkout. Proceed.

## Step 1: Create Isolated Workspace

### 1a. Native Worktree Tools (preferred)

Use your platform's native worktree tooling (e.g. `EnterWorktree`, workspace commands). If available, skip to setup.

### 1b. Git Worktree Fallback

Only use this if no native tool is available.

**Directory selection priority:**
1. User-declared preference in instructions
2. `.worktrees/` (hidden, preferred)
3. `worktrees/` (alternative)
4. `~/.config/superpowers/worktrees/<project>/` (global legacy)
5. Default to `worktrees/` at project root

**Safety verification** (project-local only): Verify directory is in `.gitignore` before creating worktree. If NOT ignored, add to `.gitignore`, commit, then proceed.

```bash
git worktree add "<path>/<branch-name>" -b "<branch-name>"
```

**Sandbox fallback**: If `git worktree add` fails with permission error, inform user and work in-place.

## Step 2: Project Setup

Auto-detect and run setup:

```bash
# Node.js
if [-f package.json]; then npm install; fi
# Python
if [-f requirements.txt]; then pip install -r requirements.txt; fi
```

## Step 3: Verify Clean Baseline

Run tests to ensure workspace starts clean:

```bash
npm test / cargo test / pytest
```

**If tests fail**: Report failures, ask whether to proceed or investigate.
**If tests pass**: Report ready.

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation (Step 0) |
| Native worktree tool available | Use it (Step 1a) |
| No native tool | Git worktree fallback (Step 1b) |
| `.worktrees/` exists | Use it (verify ignored) |
| Permission error on create | Sandbox fallback, work in-place |
| Tests fail at baseline | Report + ask |

## Red Flags

**Never:**
- Create a worktree when Step 0 detects existing isolation
- Use `git worktree add` when you have a native tool
- Skip baseline test verification
- Proceed with failing tests without asking
- Create worktree without verifying it's in `.gitignore` (project-local)
