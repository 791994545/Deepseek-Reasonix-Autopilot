---
name: gitnexus-impact-analysis
description: Analyze code change impact before editing. Use when the user asks "Is it safe to change X?", "What depends on this?", "What will break?", or before making non-trivial code changes to understand the blast radius. Requires GitNexus index.
allowed-tools: run_command,read_file
---

<MANDATORY_EXECUTION_SCRIPT>
1. `npx gitnexus status` → Check index freshness → `[√]`
2. `gitnexus_impact({target: "X", direction: "upstream"})` → Find dependents → `[√]`
3. Review risks: d=1 WILL BREAK, d=2 LIKELY AFFECTED, d=3 MAY NEED TESTING → `[√]`
4. read_file affected process resources → Check execution flows → `[√]`
5. `gitnexus_detect_changes()` → Pre-commit check on changes → `[√]`
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full reference.
