# Daily Summary to Notion — Setup Guide

## Overview

This system lets you log daily work summaries from Claude Code to Notion and auto-generates weekly reports for your supervisor. It supports marking personal project content so it's excluded from weekly reports.

## Prerequisites

- Claude Code CLI installed (`winget install Anthropic.ClaudeCode` or see [install docs](https://code.claude.com/docs/en/quickstart.md))
- A Notion account with a workspace

## Step 1: Connect Notion to Claude Code

Add the official Notion MCP server:

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

Then authenticate inside Claude Code:

```
/mcp
```

Select **Notion** and complete the OAuth flow in your browser.

## Step 2: Create Notion Databases

Create **two databases** in your Notion workspace:

### Daily Summaries Database

Create a full-page database with these properties:

| Property   | Type     | Description                                     |
|------------|----------|-------------------------------------------------|
| `Name`     | Title    | Auto-filled (default)                           |
| `Date`     | Date     | The day this summary covers                     |
| `Week`     | Text     | ISO week string, e.g., "2026-W12"               |
| `Excluded` | Checkbox | If checked, entire day excluded from weekly report |

### Weekly Summaries Database

Create a full-page database with these properties:

| Property       | Type | Description                              |
|----------------|------|------------------------------------------|
| `Name`         | Title| Auto-filled (default)                    |
| `Week`         | Text | ISO week string, e.g., "2026-W12"        |
| `Date Range`   | Text | e.g., "2026-03-11 to 2026-03-17"         |
| `Generated At` | Date | When the report was auto-generated        |

**Important:** Make sure both databases are shared with the Notion integration (click "..." menu > "Connections" > add your integration).

## Step 3: Configure the Workspace

Run inside Claude Code:

```
/configure-notion
```

This will ask you for:
1. Daily Summaries Database ID (from the Notion URL)
2. Weekly Summaries Database ID
3. Workspace name (optional)
4. Weekly report schedule — day & time (e.g., "Tuesday 19:00", "Friday 17:00")

The config is saved to `.claude/config/notion-config.json`.

### Finding Your Database ID

Open the database as a full page in Notion. The URL looks like:
```
https://www.notion.so/yourworkspace/abc123def456...?v=...
```
The 32-character hex string before `?` is your database ID.

## Step 4: Verify the Scheduled Task

The weekly report task is pre-configured. To verify:

- Check the "Scheduled" section in the Claude Code sidebar
- The task `weekly-summary-report` should show the next run time

**Recommended:** Click "Run now" once to pre-approve the tools the task needs. This prevents future automatic runs from pausing on permission prompts.

### Changing the Schedule

1. Run `/configure-notion` and update the schedule
2. Then ask Claude: "Update the weekly-summary-report scheduled task to run on [day] at [time]"

## Usage

### Log a Work Session

After working in Claude Code, run:

```
/summarize-to-notion
```

Claude will summarize what you did in this session and write it to today's daily summary page.

### Log a Personal Project Session

If the current session is for a personal project (not for the weekly report):

```
/summarize-to-notion --personal
```

Or use the shortcut:

```
/summarize-to-notion-personal
```

This wraps the summary under a `## Personal Notes` heading and marks the day as excluded.

### Mixed Sessions

If a day has both research and personal work:
- Run `/summarize-to-notion` for research sessions (no flag)
- Run `/summarize-to-notion --personal` for personal sessions

Within a single daily page, only the `## Personal Notes` sections are stripped from the weekly report. Non-personal sessions on the same day are still included.

### Manually Add Personal Sections

You can also manually add `## Personal Notes` headings in Notion. Any content under this heading (until the next `##` or `#` heading) will be excluded from the weekly report.

### Generate Weekly Report Manually

```
/weekly-summary
```

Or for a specific past week:

```
/weekly-summary 2026-W11
```

### Automatic Weekly Reports

The scheduled task runs at your configured time (default: every Tuesday at 7pm). It generates the weekly summary and saves it to the weekly database automatically.

## File Structure

```
.claude/
├── config/
│   └── notion-config.json          # Workspace & schedule configuration
└── skills/
    ├── summarize-to-notion/
    │   └── SKILL.md                 # Daily summary command
    ├── summarize-to-notion-personal/
    │   └── SKILL.md                 # Personal summary shortcut
    ├── configure-notion/
    │   └── SKILL.md                 # Workspace configuration command
    └── weekly-summary/
        └── SKILL.md                 # Weekly report generator
```

## Personal Content Convention

The system uses a **heading-based convention** to mark personal content:

```markdown
## Session - 14:30
Worked on implementing the new data pipeline for the research project.

## Personal Notes

### Session - 16:00
Fixed a bug in my personal portfolio website.
Set up CI/CD for my side project.

## Session - 18:00
Ran experiments with the updated model parameters.
```

In the example above, only the "Session - 14:30" and "Session - 18:00" content will appear in the weekly report. The "Personal Notes" section is stripped.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Notion not configured" | Run `/configure-notion` |
| Notion MCP not connected | Run `/mcp` and authenticate Notion |
| Database not accessible | Share the database with the Notion integration in Notion's connection settings |
| Scheduled task not running | Check the Scheduled section in sidebar; click "Run now" to pre-approve tools |
| Wrong week range | Check `weekly_report_schedule.day` in config matches your reporting cycle |
