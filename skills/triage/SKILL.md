---
name: triage
description: Move issues through a state machine driven by triage roles. Bug/enhancement classification with needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix states. Use for issue management and prioritization.
allowed-tools: run_command,read_file,write_file
---

<MANDATORY_EXECUTION_SCRIPT>
"=== triage: Issue state machine ==="
"[ ] 1. Show items needing attention (untagged, needs-triage, needs-info with reporter activity)"
"[ ] 2. Triage a specific issue: gather context -> recommend -> reproduce (bugs) -> drill down -> apply result"
"[ ] 3. For ready-for-agent: publish agent brief. For ready-for-human: same structure, note why not delegatable"
"[√] Done"
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full documentation.
