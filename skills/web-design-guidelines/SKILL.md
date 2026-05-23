---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

<MANDATORY_EXECUTION_SCRIPT>
# Web Design Guidelines Execution Script
# Run each step in order. Each must output [√] before proceeding.

Write-Progress "Web Design Guidelines Step 1/4 — Fetch Guidelines"
# Fetch latest guidelines from source URL
Write-Output "[√] Step 1: Fetch guidelines from source URL"

Write-Progress "Web Design Guidelines Step 2/4 — read_file Files"
# read_file the specified files (or prompt user for files/pattern)
Write-Output "[√] Step 2: read_file specified files"

Write-Progress "Web Design Guidelines Step 3/4 — Check Rules"
# Check against all rules in the fetched guidelines
Write-Output "[√] Step 3: Check against all rules"

Write-Progress "Web Design Guidelines Step 4/4 — Output Findings"
# Output findings in the terse `file:line` format
Write-Output "[√] Step 4: Output findings"
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full documentation.
