---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work — guides merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling the chosen workflow.

**Core principle**: Verify tests → Detect environment → Present options → Execute choice → Clean up.

**Announce at start**: "I'm using the finishing-a-development-branch skill to complete this work."

## Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:
[Show failures]
Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

## Step 2: Detect Environment

Determine workspace state:

```bash
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null && pwd -P)
GIT_COMMON=$(git rev-parse --git-common-dir 2>/dev/null && pwd -P)
```

| State | Menu | Cleanup |
|-------|------|---------|
| Normal repo | Standard 4 options | No worktree to clean |
| Named branch worktree | Standard 4 options | Provenance-based (see Step 6) |
| Detached HEAD worktree | Reduced 3 options (no merge) | No cleanup (externally managed) |

## Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main/master — is that correct?"

## Step 4: Present Options

**Normal repo and named-branch worktree — present exactly these 4 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Detached HEAD — present exactly these 3 options:**
```
1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work
```

Don't add explanation — keep options concise.

## Step 5: Execute Choice

### Option 1: Merge Locally

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch>
git pull
git merge <feature-branch>
# Verify tests on merged result
<test command>
# Only after merge succeeds: cleanup worktree (Step 6), delete branch
git branch -d <feature-branch>
```

### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "<summary>"
```

**Do NOT clean up worktree** — user needs it alive to iterate on PR feedback.

### Option 3: Keep As-Is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

**Don't clean up worktree.**

### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for typed confirmation.

If confirmed:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```
Then: Cleanup worktree (Step 6), force-delete branch:
```bash
git branch -D <feature-branch>
```

## Step 6: Cleanup Workspace

**Only runs for Options 1 and 4.** Options 2 and 3 always preserve the worktree.

```bash
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null && pwd -P)
GIT_COMMON=$(git rev-parse --git-common-dir 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**If normal repo (`GIT_DIR == GIT_COMMON`):** No worktree to clean. Done.

**If worktree is under `worktrees/`, `.worktrees/`, or `~/.config/superpowers/worktrees/`:** Superpowers created it — we own cleanup.
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up stale registrations
```

**Otherwise:** The host environment created this workspace. Do NOT remove it. If your platform provides a workspace-exit tool, use it. Otherwise leave the workspace in place.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | yes | - |
| 3. Keep as-is | - | - | yes | - |
| 4. Discard | - | - | - | yes (force) |

## Common Mistakes

- **Skipping test verification**: Merge broken code, create failing PR
- **Open-ended questions**: "What should I do next?" is ambiguous — present exactly 4 structured options
- **Cleaning up worktree for Option 2**: User needs it for PR iteration
- **Deleting branch before removing worktree**: `git branch -d` fails because worktree references the branch
- **Running `git worktree remove` from inside the worktree**: Fails silently — always `cd` to main repo root first
- **Cleaning up harness-owned worktrees**: Only clean ones under `worktrees/` or `.worktrees/`

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on merged result
- Delete work without typed confirmation
- Force-push without explicit request
- Remove a worktree before confirming merge success
- Clean up worktrees you didn't create (provenance check)
- Run `git worktree remove` from inside the worktree

**Always:**
- Verify tests before offering options
- Detect environment before presenting menu
- Present exactly 4 options (or 3 for detached HEAD)
- Get typed confirmation for discard
- Clean up worktree for Options 1 & 4 only
- `cd` to main repo root before worktree removal
- Run `git worktree prune` after removal
