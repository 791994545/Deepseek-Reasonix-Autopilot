---
name: gitnexus-refactoring
description: "Use when the user wants to rename, extract, split, move, or restructure code safely. Examples: \"Rename this function\", \"Extract this into a module\", \"Refactor this class\", \"Move this to a separate file\"."
---

<MANDATORY_EXECUTION_SCRIPT>
1. `gitnexus_impact({target: "X", direction: "upstream"})` → Map all dependents → `[√]`
2. `gitnexus_query({query: "X"})` → Find execution flows involving X → `[√]`
3. `gitnexus_context({name: "X"})` → See all incoming/outgoing refs → `[√]`
4. Plan update order: interfaces → implementations → callers → tests → `[√]`
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full reference.
