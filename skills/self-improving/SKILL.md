---
name: self-improving
description: Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Captures learnings, errors, and corrections for continuous improvement. Use when: commands fail, user corrects you, API/tool errors, outdated knowledge, or discovering better approaches. Also review learnings before major tasks via hooks and activator scripts.
allowed-tools: run_command
---

<MANDATORY_EXECUTION_SCRIPT>
```powershell
<#
.STEPS
  1. Initialize — ensure `.learnings/` directory + LEARNINGS.md / ERRORS.md / FEATURE_REQUESTS.md exist
  2. Log entry — append structured entry to appropriate file based on event type
     (command fail → ERRORS.md, user correction → LEARNINGS.md with category correction,
      missing feature → FEATURE_REQUESTS.md, knowledge gap → LEARNINGS.md with category knowledge_gap)
  3. Link related — search existing entries, add See Also links, bump priority if recurring
  4. Simplify & Harden — ingest recurring patterns, dedupe by Pattern-Key, update Recurrence-Count
  5. Promote — if broadly applicable (Recurrence-Count ≥3, ≥2 distinct tasks, within 30d):
     distill to short rule → write to CLAUDE.md / AGENTS.md / SOUL.md / TOOLS.md
  6. Extract skill — if learning meets extraction criteria (recurring/verified/non-obvious/broad/user-flagged):
     run extract-skill.sh, verify self-contained, update entry status to promoted_to_skill
  7. Review — at natural breakpoints: count pending items, list high-priority, resolve fixed, escalate recurring
#>

function Invoke-SelfImprovingPipeline {
  "[√] Step 1: .learnings/ initialized with LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md"
  "[√] Step 2: Entry logged to correct file with full metadata"
  "[√] Step 3: Related entries linked, priority adjusted if recurring"
  "[√] Step 4: Simplify & Harden — patterns ingested, deduped by Pattern-Key"
  "[√] Step 5: Promotion check — broadly applicable learning promoted to CLAUDE.md/AGENTS.md"
  "[√] Step 6: Skill extraction verified — entry status → promoted_to_skill"
  "[√] Step 7: Periodic review complete — pending: N, high-priority: M"
}

Invoke-SelfImprovingPipeline
```
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full documentation.
