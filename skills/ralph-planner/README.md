# Ralph Planner

**Planning-first workflows for Ralph Wiggum loops**

> Turn a vague task into a clear execution plan — then run it in a loop.

## Why Planning Matters

[Ralph Wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) is a powerful loop execution plugin that iterates until a task is complete.

For complex tasks, having a structured plan before starting the loop helps:

- Define clear scope and phases upfront
- Set verifiable completion criteria
- Estimate iterations more accurately

Ralph Planner generates structured plans designed to integrate with ralph-wiggum loops.

## Quick Start

```
/ralph-planner:plan-loop "Add user authentication with JWT"
```

That's it. You get a structured plan + a ready-to-run loop command.

## The DONE Condition (Why This Matters)

The #1 reason loops run forever: **no verifiable exit criteria**.

Ralph Planner generates commands with **specific DONE conditions**:

```
# Bad (runs forever - no completion promise)
/ralph-wiggum:ralph-loop "Implement auth" --max-iterations 30

# Good (knows when to stop)
/ralph-wiggum:ralph-loop "Implement auth. DONE when: POST /login returns 200 with valid JWT, all tests pass, invalid credentials return 401. Output <promise>COMPLETE</promise> when done." --completion-promise "COMPLETE" --max-iterations 30
```

Every template includes verifiable promises like:
- `"All tests pass"` (not "tests look good")
- `"Endpoint returns 200"` (not "endpoint works")
- `"Bug no longer reproducible"` (not "bug seems fixed")

## Installation

### In-app (recommended)

```
/plugin marketplace add vavasilva/ralph-planner
/plugin install ralph-planner@ralph-planner
```

### CLI

```bash
claude plugin marketplace add vavasilva/ralph-planner
claude plugin install ralph-planner@ralph-planner
```

### Requirement

Requires [ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum):

```
/plugin install ralph-wiggum@claude-plugins-official
```

## Demo

### Input

```
/ralph-planner:feature "Implement JWT authentication for the API"
```

### Output

```markdown
## Phase 1: Discovery
- [ ] Analyze authentication requirements
- [ ] Identify affected endpoints
- [ ] Research JWT best practices

## Phase 2: Implementation
- [ ] Create JWT generation on login
- [ ] Add validation middleware
- [ ] Secure protected routes

## Phase 3: Testing
- [ ] Write unit tests for auth logic
- [ ] Write integration tests for endpoints

## Phase 4: Documentation
- [ ] Update API documentation

Estimated iterations: 30
```

### Ready-to-run command

```
/ralph-wiggum:ralph-loop "Implement JWT auth. DONE when: POST /login returns JWT, protected routes reject invalid tokens, all tests pass. Output <promise>COMPLETE</promise> when done." --completion-promise "COMPLETE" --max-iterations 30
```

**Plan → Execute → Converge**

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-planner:plan-loop "<task>"` | Generic plan for any task |
| `/ralph-planner:feature "<desc>"` | New feature implementation |
| `/ralph-planner:bugfix "<desc>"` | Bug fix with regression test |
| `/ralph-planner:refactor "<desc>"` | Code refactoring |
| `/ralph-planner:migration "<desc>"` | Data/code migration |
| `/ralph-planner:performance "<desc>"` | Performance optimization |
| `/ralph-planner:from-file "<path>"` | Create plan from existing .md file |
| `/ralph-planner:from-issue "#123"` | Create plan from GitHub issue |
| `/ralph-planner:help` | Show help documentation |

## Specialized Templates

Each template has **pre-defined phases** and **verifiable promises**:

### Feature

```
/ralph-planner:feature "Add user authentication with JWT"
```

| Phases | Discovery → Implementation → Testing → Documentation |
|--------|-------------------------------------------------------|
| DONE when | All new tests pass, Feature works as specified, No regressions |

### Bugfix

```
/ralph-planner:bugfix "Users can't login after password reset"
```

| Phases | Reproduction → Root Cause → Fix → Verification |
|--------|------------------------------------------------|
| DONE when | Bug no longer reproducible, Regression test added, No new issues |

### Refactor

```
/ralph-planner:refactor "Extract payment logic into separate service"
```

| Phases | Analysis → Preparation → Refactor → Validation |
|--------|------------------------------------------------|
| DONE when | All existing tests pass, No behavior changes, Goals met |

### Migration

```
/ralph-planner:migration "Move user data from MySQL to PostgreSQL"
```

| Phases | Assessment → Preparation → Migration → Verification |
|--------|-----------------------------------------------------|
| DONE when | All data migrated, Application functional, Rollback tested |

### Performance

```
/ralph-planner:performance "Reduce API response time for /users endpoint"
```

| Phases | Baseline → Analysis → Optimization → Validation |
|--------|--------------------------------------------------|
| DONE when | Response time < target, No regressions, Benchmarks documented |

### From File

Already have a feature spec documented? Generate a plan from it:

```
/ralph-planner:from-file "./docs/my-feature.md"
/ralph-planner:from-file "./issues/bug-123.md" --type bugfix
/ralph-planner:from-file "./docs/feature.md" --output "./plans/feature-plan.md"
```

### From Issue

Create plans directly from GitHub issues. Labels auto-detect the work type:

```
/ralph-planner:from-issue "#42"
/ralph-planner:from-issue "owner/repo#123"
/ralph-planner:from-issue "#42" --include-comments
```

**Auto-detection from labels:**

| GitHub Labels | Template |
|---------------|----------|
| `bug`, `bugfix`, `fix` | bugfix |
| `enhancement`, `feature` | feature |
| `refactor`, `tech-debt` | refactor |
| `migration`, `upgrade` | migration |
| `performance`, `perf` | performance |

## Why Templates?

Generic promises like *"I will complete all phases systematically"* are **not verifiable**.

Templates provide:

- **Specific phases** for each work type
- **Verifiable DONE conditions** ("All tests pass" vs "I'll do my best")
- **Exit criteria** that tell the loop when to stop

## How It Works

Understanding the workflow is important:

### What ralph-planner does

1. **Generates a detailed plan** (phases, tasks, criteria) — for YOU to review
2. **Creates a summary prompt** with DONE conditions — for ralph-loop to execute

### What ralph-loop receives

Ralph-loop only receives the **summary prompt**, not the detailed plan:

```
/ralph-wiggum:ralph-loop "Implement auth. DONE when: login works, tests pass..."
```

Claude in the loop sees this summary, not the 4 phases with 15 tasks.

### When to use `--output`

For **complex tasks**, save the plan to a file so Claude can reference it:

```bash
# 1. Generate and save plan
/ralph-planner:feature "Add authentication" --output "./plans/auth.md"

# 2. Generated command references the file
/ralph-wiggum:ralph-loop "Implement auth from ./plans/auth.md. DONE when: ..."
```

Now Claude can **read the plan file** during execution to see detailed phases and tasks.

### Simple vs Complex

| Task Complexity | Recommendation |
|-----------------|----------------|
| Simple (1-5 tasks) | Summary prompt is enough |
| Complex (10+ tasks, multiple phases) | Use `--output` for detailed reference |

## How It Fits the Ralph Ecosystem

| Tool | Role |
|------|------|
| ralph-wiggum | Execution loop |
| ralph-planner | Planning & scope definition |
| You | Decide when to run |

Ralph Planner does **not** compete with ralph-wiggum — it **makes it better**.

## Running Unattended Loops

For long-running loops without permission prompts:

```bash
claude --dangerously-skip-permissions
```

> **Warning:** This skips ALL permission checks. Only use in:
> - Isolated/sandboxed environments
> - Projects where you trust the plan completely
> - When you've reviewed the generated plan first

**Recommended workflow:**

1. Generate plan with ralph-planner (review it carefully)
2. Start Claude with `--dangerously-skip-permissions`
3. Run the ralph-loop command

## Roadmap

- [ ] Configurable iteration multiplier (`--multiplier`) [#2](https://github.com/vavasilva/ralph-planner/issues/2)
- [ ] Risk & dependency section in plans [#3](https://github.com/vavasilva/ralph-planner/issues/3)
- [ ] Machine-readable plan format (YAML/JSON) [#4](https://github.com/vavasilva/ralph-planner/issues/4)
- [ ] Custom template creation [#5](https://github.com/vavasilva/ralph-planner/issues/5)

## Troubleshooting

### Loop runs infinitely / "No completion promise set"

If you see this message repeatedly:
```
Ralph iteration X | No completion promise set - loop runs infinitely
```

The ralph-wiggum plugin saves state in `.claude/ralph-loop.local.md`. If a loop wasn't properly cancelled, it persists.

**Solution:**

1. Cancel the active loop:
   ```
   /ralph-wiggum:cancel-ralph
   ```

2. Or delete the state file manually:
   ```bash
   rm .claude/ralph-loop.local.md
   ```

3. Start a fresh Claude session

### Plan generates but loop starts automatically

If planning triggers automatic execution, there's likely an active loop from a previous session. Cancel it first using the steps above.

## License

MIT
