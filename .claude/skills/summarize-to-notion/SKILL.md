---
name: summarize-to-notion
description: Summarize the current Claude session and create/update a daily summary in the configured Notion workspace. Use when the user wants to log their work to Notion. Supports --personal flag to mark content as excluded from weekly reports.
argument-hint: "[--personal]"
disable-model-invocation: true
allowed-tools: Read, Bash, Grep, Glob
---

# Summarize Session to Notion

## Instructions

You are summarizing what was accomplished in the current Claude Code session and writing it to a Notion daily summary.

### Step 1: Read Configuration

Read the Notion configuration from `${CLAUDE_SKILL_DIR}/../../config/notion-config.json`.

If the file is missing or `daily_database_id` is empty, tell the user:
> "Notion is not configured yet. Please run `/configure-notion` first to set up your workspace."

Then stop.

If `weekly_report_schedule.day` or `weekly_report_schedule.time` is empty (first-time use), ask the user:
> "It looks like this is your first time using the summary system. When would you like your weekly report to be generated automatically? Please provide a day and time (e.g., 'Tuesday 19:00' or 'Friday 17:00')."

Save their answer to the config file's `weekly_report_schedule` fields, then continue with the summarization. Also remind the user they can change this later via `/configure-notion`.

### Step 2: Check for --personal Flag

Check if `$ARGUMENTS` contains `--personal`.

- If `--personal` is present, this session's summary will be wrapped under a `## Personal Notes` heading and the database entry will have `Excluded` set to `true`.

### Step 3: Summarize the Session

Reflect on the current conversation and generate a concise, informative summary covering:

- **What was worked on**: files modified, features added, bugs fixed, research done
- **Key decisions made**: architectural choices, trade-offs discussed
- **Outcomes**: what was accomplished, what's left to do
- **Tools/technologies used**: languages, frameworks, libraries involved

Keep the summary professional and useful for a weekly research report context. Write in past tense. Be specific about what was done rather than vague.

### Step 4: Check for Existing Daily Entry

Use the Notion MCP tools to query the daily summaries database (from config) for an entry with today's date.

- If an entry **exists**: append the new session summary to the existing page content, under a new `## Session - HH:MM` heading (using current time).
- If **no entry exists**: create a new database entry with:
  - `Date`: today's date
  - `Week`: current ISO week string (e.g., "2026-W12")
  - `Excluded`: `true` if `--personal` flag was used, `false` otherwise
  - Page content: the session summary under a `## Session - HH:MM` heading

### Step 5: Handle Personal Content

If `--personal` flag is active:
- Wrap the entire session summary content inside a `## Personal Notes` section
- Format:
  ```
  ## Personal Notes

  ### Session - HH:MM
  [summary content here]
  ```
- Set the `Excluded` property to `true` on the database entry

If NOT personal:
- Use the normal format:
  ```
  ## Session - HH:MM
  [summary content here]
  ```

### Step 6: Confirm to User

After writing to Notion, confirm:
- What was written
- Which database entry (date)
- Whether it was marked as personal/excluded
- A brief preview of the summary (2-3 sentences)

## Important Notes

- If the Notion MCP server is not connected, instruct the user to run `/mcp` to authenticate.
- Always use the database ID from the config file, never hardcode IDs.
- The `## Personal Notes` heading convention is critical — the weekly summary skill relies on it to filter content.
- When appending to an existing day, preserve all existing content and add the new session below it.
- If a day already has `Excluded = true` and the new session is NOT personal, keep `Excluded = true` (once excluded, stays excluded for the whole day unless manually changed).
