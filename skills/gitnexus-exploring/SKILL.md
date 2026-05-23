---
name: gitnexus-exploring
description: Explore and understand unfamiliar codebases using GitNexus. Use when the user asks "How does X work?", "What calls this function?", "Show me the auth flow", "What's the project structure?", or when understanding code you haven't seen before.
allowed-tools: read_file,run_command
---

<MANDATORY_EXECUTION_SCRIPT>
1. read_file `gitnexus://repos` → Discover indexed repos → `[√]`
2. read_file `gitnexus://repo/{name}/context` → Get codebase stats and staleness → `[√]`
3. `gitnexus_query({query: "<concept>"})` → Find related execution flows → `[√]`
4. `gitnexus_context({name: "<symbol>"})` → 360-degree symbol view → `[√]`
5. read_file `gitnexus://repo/{name}/process/{name}` → Trace full step-by-step flows → `[√]`
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full reference.
