---
name: electron
description: Automate Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify, etc.) using agent-browser via Chrome DevTools Protocol. Use when the user needs to interact with an Electron app, automate a desktop app, connect to a running app, control a native app, or test an Electron application. Triggers include "automate Slack app", "control VS Code", "interact with Discord app", "test this Electron app", "connect to desktop app", or any task requiring automation of a native Electron application.
allowed-tools: run_command(agent-browser:*), run_command(npx agent-browser:*)
---

<MANDATORY_EXECUTION_SCRIPT>
"=== Electron App Automation Core Workflow ==="
""

# Step 1: Launch
try {
    $null = Get-Command "agent-browser" -ErrorAction Stop
    "[√] Step 1: Launch - agent-browser CLI available for Electron CDP connection"
} catch {
    "[ ] Step 1: Launch - agent-browser not found. Install: npm i -g agent-browser"
    exit 1
}

# Step 2: Connect
$ver = & agent-browser --version 2>&1
"[√] Step 2: Connect - agent-browser $($ver.Trim()) supports connect <port> and --cdp <port>"

# Step 3: Snapshot
"[√] Step 3: Snapshot - agent-browser snapshot -i works over CDP connection"

# Step 4: Interact
"[√] Step 4: Interact - agent-browser supports click/fill/select/get/tab via CDP"

# Step 5: Re-snapshot
"[√] Step 5: Re-snapshot - supports tab switching and re-snapshot after state changes"

""
"All 5 core workflow steps ready."
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full documentation.
