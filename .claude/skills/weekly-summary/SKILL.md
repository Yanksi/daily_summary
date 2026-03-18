---
name: weekly-summary
description: Generate a weekly summary from daily Notion summaries, excluding personal content. Runs automatically on the configured schedule (default Tuesday 7pm) or can be invoked manually. Used for PhD weekly supervisor reports.
disable-model-invocation: true
allowed-tools: Read, Bash, Grep, Glob
---

# Generate Weekly Summary

## Instructions

Generate a cohesive weekly report from the daily summaries stored in Notion, suitable for a PhD student's weekly supervisor report.

### Step 1: Read Configuration

Read `~/.claude/config/notion-config.json` (i.e. `$HOME/.claude/config/notion-config.json`).

If not configured, tell the user to run `/configure-notion` first and stop.

### Step 2: Determine the Week Range

Read the `weekly_report_schedule.day` from the config to determine the reporting cycle. The week range ends on the scheduled day (inclusive) and starts 7 days before.

For example, if the schedule is Tuesday:
- The week runs **Wednesday to Tuesday** (since the report is due Tuesday evening)
- Find last Wednesday's date through today (Tuesday)

If the schedule is Friday:
- The week runs **Saturday to Friday**

Format as ISO week string (e.g., "2026-W12").

If `$ARGUMENTS` contains a specific week string (e.g., "2026-W11"), use that instead to generate a report for a past week.

### Step 3: Fetch Daily Summaries

Query the daily summaries database for all entries where:
- `Date` falls within the calculated week range (Wednesday to Tuesday)

Read the full page content of each matching entry.

### Step 4: Filter Out Personal Content

For each daily summary:

1. **Check the `Excluded` property**: If `Excluded = true`, skip the entire day's entry.
2. **Strip `## Personal Notes` sections**: For non-excluded entries, remove any content that falls under a `## Personal Notes` heading. The personal section extends from the `## Personal Notes` heading until:
   - The next heading of the same level (`##`) or higher level (`#`), OR
   - The end of the page content if no such heading follows
3. Keep all other content intact.

### Step 5: Generate the Weekly Report

Synthesize the filtered daily summaries into a cohesive weekly report structured as:

```markdown
# Weekly Summary: [Week String] ([Date Range])

## Overview
[2-3 sentence high-level summary of the week's work]

## Research Progress
[Key research activities, experiments, findings]

## Technical Work
[Code written, tools built, infrastructure changes]

## Key Decisions & Insights
[Important decisions made, lessons learned, insights gained]

## Challenges & Blockers
[Any issues encountered, pending questions]

## Next Steps
[What's planned for the coming week, if mentioned in any daily notes]
```

Guidelines for the report:
- Write in professional academic tone suitable for a supervisor
- **Use bullet points** within each section — no long prose paragraphs
- Be specific — reference concrete results, not vague descriptions
- Consolidate related work across days; combine rather than repeat
- **Omit minor/iterative details**: doc tweaks, small refactors, formatting fixes, intermediate debugging steps should not appear unless they were a major focus
- Keep total length concise (aim for 200-400 words)
- Omit empty sections rather than writing "Nothing this week"

### Step 6: Write to Notion

Query the weekly summaries database for an existing entry where `Week` matches the current week string.

- If an entry **exists**: update the existing page by replacing its content with the new report, and update the `Generated At` property to the current date/time.
- If **no entry exists**: create a new entry with:
  - `Week`: the week string (e.g., "2026-W12")
  - `Date Range`: the date range string (e.g., "2026-03-11 to 2026-03-17")
  - `Generated At`: current date/time
  - Page content: the generated weekly report

This makes the operation idempotent — running it multiple times for the same week simply updates the existing entry.

### Step 7: Confirm

Tell the user:
- Weekly summary has been generated and saved
- Which days were included (and which were excluded)
- How many session entries were processed
- A brief preview of the overview section

## Important Notes

- This skill is also triggered automatically via a scheduled task at the time configured in `notion-config.json` (default: Tuesday 7pm).
- The `## Personal Notes` heading convention must be respected exactly — this is the contract between the daily and weekly skills.
- If no daily summaries exist for the week, create a minimal entry noting "No daily summaries were recorded this week."
