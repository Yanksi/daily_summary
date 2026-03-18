---
name: summarize-to-notion-personal
description: Shortcut for /summarize-to-notion --personal. Summarizes the current session and marks it as personal/excluded from weekly reports.
disable-model-invocation: true
allowed-tools: Read, Bash, Grep, Glob
---

# Summarize Session to Notion (Personal)

This is a convenience shortcut. Execute the exact same behavior as `/summarize-to-notion --personal`.

Read and follow all instructions from the skill file at `${CLAUDE_SKILL_DIR}/../summarize-to-notion/SKILL.md`, treating the `--personal` flag as active regardless of `$ARGUMENTS`.

Everything in this session's summary will be wrapped under `## Personal Notes` and the daily entry will be marked as `Excluded = true`.
