---
name: to-prd
description: Convert the current conversation context into a structured PRD and publish to the issue tracker. No extra questioning - work from what's already in context.
allowed-tools: read_file,write_file
---

<MANDATORY_EXECUTION_SCRIPT>
"=== to-prd: Convert conversation to PRD ==="
"[ ] 1. Explore codebase - Understand current state"
"[ ] 2. Sketch modules - List modules to build/modify"
"[ ] 3. Confirm with user - Module breakdown and testing preferences"
"[ ] 4. write_file and publish PRD - Include problem statement, solution, user stories, implementation decisions, testing decisions, out-of-scope"
"[√] Done"
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full documentation.
