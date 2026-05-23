# ralph-planner

## Overview
Companion plugin for [ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) that creates structured plans in Ralph format and auto-generates loop commands.

## Location
`~/Code/ralph-planner`

## Structure
```
ralph-planner/
├── .claude-plugin/
│   ├── plugin.json        # Plugin metadata
│   └── marketplace.json   # Marketplace configuration
├── commands/
│   ├── plan-loop.md       # Generic planning
│   ├── feature.md         # Feature template
│   ├── bugfix.md          # Bugfix template
│   ├── refactor.md        # Refactor template
│   ├── migration.md       # Migration template
│   ├── performance.md     # Performance template
│   ├── from-file.md       # Plan from .md file
│   ├── from-issue.md      # Plan from GitHub issue
│   └── help.md            # Help documentation
└── README.md
```

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-planner:plan-loop "<task>"` | Generic plan for any task |
| `/ralph-planner:feature "<desc>"` | New feature implementation |
| `/ralph-planner:bugfix "<desc>"` | Bug fix with regression test |
| `/ralph-planner:refactor "<desc>"` | Code refactoring |
| `/ralph-planner:migration "<desc>"` | Data/code migration |
| `/ralph-planner:performance "<desc>"` | Performance optimization |
| `/ralph-planner:from-file "<path>"` | Create plan from .md file |
| `/ralph-planner:from-issue "#123"` | Create plan from GitHub issue |
| `/ralph-planner:help` | Show help documentation |

## Key Features
- Work type templates with pre-defined phases
- Verifiable promises (not generic statements)
- Auto-detection from GitHub labels (from-issue)
- Estimates iterations based on task count (tasks × 3)
- Generates ready-to-run `/ralph-wiggum:ralph-loop` commands

## Dependencies
- Requires [ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) plugin

## Installation
```bash
claude plugin marketplace add vavasilva/ralph-planner
claude plugin install ralph-planner@ralph-planner
```

## GitHub
https://github.com/vavasilva/ralph-planner
