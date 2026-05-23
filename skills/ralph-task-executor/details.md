# Ralph Task Executor

Relentless task execution engine. No pauses, no confirmations, no giving up.

## When to Use

- User says "execute tasks", "run tasks", "just do it", "no stopping"
- Tasks have been planned by ralph-planner and need execution
- Long task list that must complete without human intervention
- CI/CD-like batch execution of code changes
- Any scenario where stopping to ask questions wastes more time than a wrong guess

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Task Executor Core                  │
│                                                      │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐ │
│  │ Priority  │──▶│  State   │──▶│  Execution       │ │
│  │ Queue     │   │ Machine  │   │  Engine          │ │
│  └──────────┘   └──────────┘   └──────────────────┘ │
│       │              │               │               │
│       ▼              ▼               ▼               │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐ │
│  │ Parallel  │   │ Safety   │   │  Output          │ │
│  │ Scheduler │   │ Guard    │   │  Formatter       │ │
│  └──────────┘   └──────────┘   └──────────────────┘ │
└─────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
  ralph-planner              ralph-loop-setup
  (task source)              (TDD integration)
```

## Execution State Machine

```
  ┌──────┐
  │ IDLE │ ◀──────────────────────────────────┐
  └──┬───┘                                     │
     │ receive_task_list                        │
     ▼                                         │
  ┌──────────┐                                  │
  │ PLANNING │ order by priority, detect deps   │
  └────┬─────┘                                  │
       │ tasks_ordered                           │
       ▼                                         │
  ┌───────────┐     retry < MAX_RETRIES    ┌────┴─────┐
  │ EXECUTING │────────────────────────────▶│ VERIFYING │
  └─────┬─────┘                             └────┬─────┘
        │ error & retries exhausted               │
        ▼                                         │ verify_pass
  ┌───────────┐                             ┌─────▼──────┐
  │  FAILED   │                             │    DONE    │
  └───────────┘                             └────────────┘
```

### State Transitions

| From | To | Trigger | Action |
|------|----|---------|--------|
| IDLE | PLANNING | Task list received | Sort by priority, detect independent tasks |
| PLANNING | EXECUTING | Order established | Pick highest-priority ready task |
| EXECUTING | VERIFYING | Task code written | Run tests / build / lint |
| VERIFYING | DONE | All checks pass | Mark complete, pick next task |
| VERIFYING | EXECUTING | Check fails, retries < MAX | Fix and retry |
| VERIFYING | FAILED | Retries exhausted | Log error, mark failed, pick next task |
| DONE | IDLE | All tasks processed | Output completion report |
| FAILED | IDLE | All tasks processed | Output report with failures |

### MAX_RETRIES per Priority

| Priority | MAX_RETRIES | Rationale |
|----------|-------------|-----------|
| P0 | 8 | Critical: keep trying harder |
| P1 | 5 | High: standard retry budget |
| P2 | 3 | Medium: limited retries |
| P3 | 2 | Low: fail fast, move on |

## Task Priority Strategy

### Priority Levels

| Level | Label | Criteria | Example |
|-------|-------|----------|---------|
| P0 | 紧急 | Blocks all other work; production down | Fix build-breaking import error |
| P1 | 高 | Blocks specific feature; user-visible | Implement auth flow |
| P2 | 中 | Feature work; not blocking others | Add pagination to list view |
| P3 | 低 | Nice-to-have; refactor; cleanup | Rename variable for clarity |

### Priority Assignment Rules

1. **Explicit**: If user or planner assigns priority, use it
2. **Implicit - Dependency**: If task A blocks task B, A gets higher priority
3. **Implicit - Scope**: Tasks touching core/shared code get +1 priority
4. **Implicit - Risk**: Tasks with unclear requirements get -1 priority (do known tasks first)
5. **Default**: P2 for all unclassified tasks

### Dependency Resolution

```json
{
  "task_id": "T003",
  "depends_on": ["T001", "T002"],
  "priority": "P1",
  "parallel_group": null
}
```

- Tasks with no dependencies and same priority can run in parallel
- Tasks with dependencies wait until all dependencies reach DONE state
- Circular dependencies → break by demoting lowest-priority edge to P3

## Parallel Execution Strategy

### Independent Task Detection

Tasks are parallelizable when:
1. They modify different files (no write conflict)
2. They have no dependency relationship
3. They share no mutable state (no global variable mutation)

### Parallel Group Assignment

```
Group A (parallel): [T001, T002, T003]  ← independent, different files
Group B (sequential): [T004]             ← depends on Group A output
Group C (parallel): [T005, T006]         ← independent, different files
Group D (sequential): [T007]             ← depends on Group C output
```

### Parallel Execution Rules

1. Max 3 concurrent tasks (avoid context thrashing)
2. If any task in a parallel group fails → stop remaining tasks in group
3. Parallel tasks must not modify the same file
4. When in doubt about independence → execute sequentially

## Output Templates

### Progress Bar Format

```
⚡ Ralph Executor ─────────────────────────────
▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  55%  6/11 tasks

✅ T001 [P0] Fix build error
✅ T002 [P1] Add auth middleware
✅ T003 [P1] Implement login API
🔄 T004 [P1] Add login UI ← current
⏳ T005 [P2] Add pagination
⏳ T006 [P2] Style dashboard
❌ T007 [P3] Rename utils (skipped: dep failed)
⏳ T008 [P2] Add tests
⏳ T009 [P3] Update comments
⏳ T010 [P2] Fix lint warnings
⏳ T011 [P3] Clean up imports
───────────────────────────────────────────────
```

### Task Completion Line

```
✅ T004 [P1] Add login UI (3 files, 2m14s)
```

### Error Line

```
⚠️ T007 [P3] Rename utils → Error: file not found → Retrying (2/2)...
```

### Final Report

```
⚡ Execution Complete ─────────────────────────
Total: 11 | ✅ Done: 8 | ❌ Failed: 1 | ⏭️ Skipped: 2
Duration: 12m37s

Failed tasks:
  ❌ T007 [P3] Rename utils — file not found after 2 retries

Skipped tasks (dependency failed):
  ⏭️ T009 — depends on T007
  ⏭️ T011 — depends on T009

Next steps:
  → Fix T007 manually, then re-run for T009, T011
───────────────────────────────────────────────
```

## Collaboration Interfaces

### With ralph-planner

```
ralph-planner ──▶ plans/prd.json ──▶ ralph-task-executor
```

- **Input**: read_file `plans/prd.json` for task list with priorities and dependencies
- **Output**: Update `plans/prd.json` task status fields as execution progresses
- **Handoff**: If planner is active, executor reads from planner's output; if no planner, executor creates its own task list from user request

### With ralph-loop-setup

```
ralph-task-executor ──▶ triggers TDD loop ──▶ ralph-loop-setup
```

- When executing a task that involves code changes, automatically trigger write-test → implement → verify cycle
- Use ralph-loop's hooks for pre-commit validation if available
- Respect ralph-loop's `watch` patterns for file change detection

### Context overflow

- If context window exceeds 60%, hand off to full-autonomous for compression
- Always write checkpoint to `plans/progress.md` before any context compression
- On recovery, read `plans/progress.md` first, then resume from last incomplete task

## Safety Boundaries

### Hard Stops (MUST pause and inform user)

1. **Data loss risk**: Operation would delete user data without backup
2. **Security exposure**: Operation would commit secrets, keys, or credentials
3. **Irreversible change**: `DROP TABLE`, `rm -rf`, force-push to main
4. **Budget risk**: Operation would trigger paid API calls > $5 without prior approval
5. **Scope creep**: Execution has expanded beyond original task by > 3x tasks

### Soft Limits (auto-handle but log)

1. **Retry exhaustion**: Mark task FAILED, continue with next
2. **Test flakiness**: If test passes 2/3 times, treat as pass and note it
3. **Ambiguous requirement**: Implement most reasonable interpretation, note assumption
4. **Dependency cycle**: Break cycle by demoting lowest-priority edge

### Rollback Strategy

When a task causes cascading failures:
1. Stop all parallel tasks in the same group
2. Revert files changed by the failing task (git checkout)
3. Mark the task and all dependents as SKIPPED
4. Continue with remaining independent tasks
5. Report rollback in final report

## Execution Rules

### 1. No Pausing
- NEVER ask for confirmation before proceeding
- NEVER stop to explain what you're about to do — just do it
- NEVER say "Would you like me to..." — always proceed
- If you need information, search for it yourself rather than asking

### 2. Error Recovery
- On error: read the error, fix it, retry
- On test failure: read the failure, fix the code, re-run
- On build failure: read the error, fix it, rebuild
- Respect MAX_RETRIES per priority level

### 3. Decision Making
- When faced with ambiguity, choose the simplest working solution
- When multiple approaches exist, pick the one most likely to work
- When unsure about requirements, implement the most reasonable interpretation
- NEVER ask "which approach do you prefer?" — pick one and go

### 4. Verification Gate
After every code change task:
1. Run relevant tests (if test framework detected)
2. Run linter (if lint command exists)
3. Run type checker (if typecheck command exists)
4. If any fail → fix and retry within budget
5. If all pass → mark DONE

## Example Scenarios

### Scenario 1: Sequential Execution with Error Recovery

```
Input: "Fix the 3 lint errors and add missing tests for utils.py"

Execution:
⚡ T001 [P1] Fix lint error: unused import in utils.py
   → edit_file utils.py, remove unused import
   → Run lint → PASS
   ✅ T001 (1 file, 0m12s)

⚡ T002 [P1] Fix lint error: missing type hint in utils.py
   → edit_file utils.py, add type hint
   → Run lint → FAIL (new error: incompatible type)
   → Fix type hint
   → Run lint → PASS
   ✅ T002 (1 file, 0m34s, 1 retry)

⚡ T003 [P1] Fix lint error: line too long in utils.py
   → edit_file utils.py, break long line
   → Run lint → PASS
   ✅ T003 (1 file, 0m08s)

⚡ T004 [P2] Add tests for utils.format_date
   → Create test_utils.py, add test cases
   → Run tests → PASS
   ✅ T004 (1 file, 0m45s)

⚡ T005 [P2] Add tests for utils.parse_input
   → Add test cases to test_utils.py
   → Run tests → PASS
   ✅ T005 (1 file, 0m38s)

⚡ Execution Complete ─────────────────────────
Total: 5 | ✅ Done: 5 | ❌ Failed: 0 | ⏭️ Skipped: 0
Duration: 2m17s
```

### Scenario 2: Parallel Execution with Dependency

```
Input: "Add user model, auth API, and profile page"

Planning:
  Group A (parallel): [T001 User Model, T002 Profile Page Mock]
  Group B (sequential): [T003 Auth API] ← depends on T001
  Group C (sequential): [T004 Wire Profile to API] ← depends on T002, T003

Execution:
🔄 T001 [P1] User Model + T002 [P2] Profile Page Mock (parallel)
   ✅ T001 (2 files, 1m05s)
   ✅ T002 (1 file, 0m52s)

🔄 T003 [P1] Auth API
   ✅ T003 (3 files, 1m30s)

🔄 T004 [P2] Wire Profile to API
   ✅ T004 (2 files, 0m48s)

⚡ Execution Complete ─────────────────────────
Total: 4 | ✅ Done: 4 | Duration: 3m15s
Parallel savings: ~1m (T001+T002 ran concurrently)
```

### Scenario 3: Safety Boundary Triggered

```
⚡ T005 [P2] Clean up old migration files
   → Detected: rm operation on migration/ directory
   → 🛑 HARD STOP: irreversible deletion without backup
   → Informing user: "T005 would delete 12 migration files. Proceed? [y/N]"
```

## Anti-Patterns (NEVER do these)

| Anti-Pattern | Do This Instead |
|-------------|----------------|
| "Shall I proceed?" | Just proceed |
| "Would you like me to also..." | Just do it |
| "I recommend..." | Just implement it |
| "There are several options..." | Pick one and implement |
| Stopping after completing a task | Start the next one immediately |
| Retrying indefinitely | Respect MAX_RETRIES, then mark FAILED |
| Running all tasks sequentially | Detect and execute independent tasks in parallel |
| Ignoring test failures | Fix and retry within budget |
| Modifying the same file in parallel | Serialize tasks that touch the same file |

## Scope

This skill ONLY:
- Executes tasks from a list without pausing for confirmation
- Manages execution state, retries, and parallel scheduling
- Reports progress and completion
- Coordinates with ralph-planner, ralph-loop, and full-autonomous

This skill NEVER:
- Plans tasks (that's ralph-planner's job)
- Modifies its own SKILL.md
- Executes tasks that trigger hard-stop safety boundaries without user consent
- Makes network requests to external services
- Accesses credentials or secrets
