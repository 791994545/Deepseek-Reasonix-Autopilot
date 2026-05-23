---
name: gitnexus-debugging
description: "Use when the user is debugging a bug, tracing an error, or asking why something fails. Examples: \"Why is X failing?\", \"Where does this error come from?\", \"Trace this bug\"."
---

<MANDATORY_EXECUTION_SCRIPT>
1. `gitnexus_query({query: "<error or symptom>"})` → Find related execution flows → `[√]`
2. `gitnexus_context({name: "<suspect>"})` → See callers/callees/processes → `[√]`
3. `READ gitnexus://repo/{name}/process/{name}` → Trace execution flow → `[√]`
4. `gitnexus_cypher({query: "MATCH path..."})` → Custom traces if needed → `[√]`
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full reference.
