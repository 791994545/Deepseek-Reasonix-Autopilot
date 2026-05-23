# Triage

Move issues on the project issue tracker through a state machine driven by triage roles.

## Roles

Two **classification** roles: `bug`, `enhancement`

Five **status** roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`

## Process

1. Show items needing attention: untagged, needs-triage, needs-info with reporter activity
2. Triage a specific issue: gather context -> recommend -> reproduce (bugs) -> drill down -> apply result
3. For `ready-for-agent`: publish agent brief. For `ready-for-human`: same structure, note why not delegatable
