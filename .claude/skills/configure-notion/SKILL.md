---
name: configure-notion
description: Configure which Notion databases to use for daily and weekly summaries. Run this once to set up or update your workspace.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

# Configure Notion Workspace

## Instructions

Help the user configure their Notion workspace for the daily/weekly summary system.

### Step 1: Check Current Config

Read `~/.claude/config/notion-config.json` (i.e. `$HOME/.claude/config/notion-config.json`) to see if there's an existing configuration.
If it exists and has values, show the current settings to the user.

### Step 2: Gather Database IDs

Ask the user to provide:

1. **Daily Summaries Database ID** — The Notion database where daily work summaries are stored.
2. **Weekly Summaries Database ID** — The Notion database where generated weekly reports go.
3. **Workspace name** (optional) — A friendly name for reference.
4. **Weekly report schedule** (required) — Day of week and time for automatic weekly report generation. There is no default — always ask the user. Format: day name + 24h time, e.g., "Tuesday 19:00" or "Friday 17:00".

Help the user find their database IDs:
- Open the database in Notion as a full page
- The URL looks like: `https://www.notion.so/workspace/DATABASE_ID?v=...`
- The DATABASE_ID is the 32-character hex string before the `?`
- It can also be passed as a full URL — extract the ID from it

### Step 3: Validate Connection

Use the Notion MCP tools to verify that both database IDs are accessible:
- Try to query each database
- If a database is not found or not accessible, inform the user and suggest they:
  - Check the database ID
  - Ensure the Notion integration has access to the database (share the database with the integration)
  - Run `/mcp` to re-authenticate if needed

### Step 4: Verify Database Properties

Check that the databases have the required properties. If missing, offer to note what needs to be added:

**Daily Summaries Database** needs:
- `Date` (date property)
- `Week` (text or formula property)
- `Excluded` (checkbox property)

**Weekly Summaries Database** needs:
- `Week` (text property)
- `Date Range` (text property)
- `Generated At` (date property)

### Step 5: Save Configuration

Write the configuration to `~/.claude/config/notion-config.json`:

```json
{
  "daily_database_id": "<extracted-id>",
  "weekly_database_id": "<extracted-id>",
  "workspace_name": "<name>",
  "weekly_report_schedule": {
    "day": "<day-of-week>",
    "time": "<HH:MM>"
  }
}
```

After saving, remind the user that if they changed the schedule, they should update or recreate the scheduled task. Provide the command:
- To update: tell Claude "update the weekly-summary-tuesday scheduled task to run on [day] at [time]"
- Or delete and recreate via the scheduled tasks system

### Step 6: Confirm

Tell the user:
- Configuration saved successfully
- Which databases are linked
- Remind them they can run `/configure-notion` again anytime to update
- Suggest running `/summarize-to-notion` to test the setup
