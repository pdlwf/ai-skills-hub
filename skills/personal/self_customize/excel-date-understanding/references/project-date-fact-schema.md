# Project-Date Fact Schema

## Purpose

This file defines the minimum structured output that the skill should extract from project schedule workbooks.

The goal is not to describe every possible field up front.

The goal is to define one stable minimum object that:

- preserves task hierarchy
- preserves parsed date meaning
- supports downstream date analysis
- works across messy but common project schedule sheets

## Design Principle

Prefer one row-level fact object per milestone row.

If one workbook row contains one child milestone, the skill should try to emit one `project_date_fact` object for that row.

If parent grouping is encoded through merged cells, that parent context should be inherited into the row-level fact object.

If note-bearing columns exist, their row-level text should be attached to the fact object as supporting evidence rather than discarded.

## Minimum Viable Object

```json
{
  "sheet": "Detailed Project schedule",
  "row": 73,
  "parent_item": "ROW-GMS SW",
  "task_key": "row-gms-sw::sw boot image, power on/off animation and wallpaper release",
  "task": "SW boot image, power on/off animation and wallpaper release",
  "owner": "UK PM",
  "planned_date": "2026-03-30",
  "actual_date": null,
  "date_status": "upcoming",
  "source_signals": [
    "cell_value",
    "conditional_formatting",
    "merged_hierarchy"
  ]
}
```

## Required Fields

- `sheet`
  - worksheet name
  - needed because row numbers alone are not globally unique

- `row`
  - 1-based worksheet row number
  - used for traceability back to the source workbook

- `parent_item`
  - parent category or workstream inherited from the grouping column
  - may be `null` if the sheet has no parent grouping

- `task_key`
  - stable logical identity for the row when safe to derive
  - use for cross-scenario comparison and stable references beyond one sheet
  - may be derived from:
    - task code
    - parent item plus normalized task name
    - another workbook-stable identifier
  - may be `null` only when no safe identity can be derived

- `task`
  - row-level child milestone or task description
  - usually comes from columns like `Milestone Details`

- `owner`
  - owner or responsible party for the row
  - may be `null` if missing

- `planned_date`
  - normalized planned schedule value
  - may be:
    - single date such as `2026-03-27`
    - date range object such as `{start, end}`
    - `null` if unresolved

- `actual_date`
  - normalized actual completion value
  - usually a single date or `null`

- `date_status`
  - normalized row-level date state
  - initial allowed values:
    - `done`
    - `completed_late`
    - `upcoming`
    - `overdue`
    - `in_progress_or_delayed`
    - `unresolved`

- `source_signals`
  - list of evidence sources used to build the fact
  - initial allowed values:
    - `cell_value`
    - `cell_text`
    - `display_format`
    - `conditional_formatting`
    - `status_text`
    - `merged_hierarchy`
    - `neighboring_context`

## Recommended Fields

These are not required for the minimum object, but the skill should add them whenever available.

- `planned_date_raw`
  - original raw workbook value before normalization

- `actual_date_raw`
  - original raw workbook value before normalization

- `planned_granularity`
  - `day`, `day-range`, `month`, `quarter`, `year`

- `actual_granularity`
  - usually `day`

- `task_code`
  - workbook-authored identifier such as `D1`, `EVT1-8`, or `MP-2`
  - preferred primary key for cross-scenario matching when present

- `task_key_source`
  - where the `task_key` came from
  - suggested values:
    - `task_code`
    - `parent_item_plus_task`
    - `task_name`
    - `manual_mapping`

- `task_key_confidence`
  - confidence in the stability of the derived task key
  - suggested values:
    - `high`
    - `medium`
    - `low`

- `workbook_status`
  - workbook-authored status such as:
    - `delay_but_manageable`
    - `blocking`
    - `due_soon_incomplete`

- `note_text`
  - original note-bearing text when it materially informs date understanding
  - may come from headers such as:
    - `remark`
    - `remarks`
    - `update`
    - `updates`
    - `feedback`
    - `updated feedback`

- `note_source_column`
  - the source header name for the extracted note text

- `note_dates`
  - extracted dates found inside note text

- `anomaly_flags`
  - any anomaly ids attached to the row
  - should reference [schedule-anomaly-schema.md](schedule-anomaly-schema.md)

## Field Semantics

### `parent_item`

This field is structural, not decorative.

If the workbook uses merged cells in the `Item` column, blank cells inside the merged block should inherit the top-cell label.

Example:

- merged range `A73:A85`
- top cell value = `ROW-GMS SW`
- all child rows in `73:85` inherit `parent_item = "ROW-GMS SW"`

### `task`

This is the child milestone, not the parent group label.

For FRM-INV style sheets:

- `parent_item` comes from `Item`
- `task` comes from `Milestone Details`

### `task_key`

This field is for stable logical identity, not user-facing display.

Preferred construction order:

- task code when present and workbook-stable
- parent item + normalized task
- normalized task only as a lower-confidence fallback

If no safe identity exists, leave it `null` and avoid cross-scenario merging.

### `planned_date`

This field should preserve parsed structure.

Examples:

- single date: `2026-03-27`
- range: `{"start":"2026-09-29","end":"2026-10-06"}`
- unresolved placeholder: `null`

### `note_text`

This field is supporting evidence.

It is especially useful when the workbook places schedule explanations in note-like columns rather than in date columns.

Examples:

- `push out from 3/20 to end of Mar because of agency priority`
- `MoU closed on 25th, Nov. 2025`
- `leaving engraving logo to be reviewed(not blocking the master plan)`

### `date_status`

This field should be derived from date evidence first, then adjusted by workbook-authored logic when explicit.

Recommended initial interpretation:

- `done`
  - actual date exists and the row is effectively completed on or before plan
- `completed_late`
  - actual date exists and is later than the planned date
- `upcoming`
  - planned date is in the future and actual date is blank
- `overdue`
  - planned date is in the past and actual date is blank
- `in_progress_or_delayed`
  - workbook logic indicates active delay-like state, but exact severity may depend on explicit status text or conditional formatting
- `unresolved`
  - date cannot yet be resolved cleanly

## Normalization Rules

- Keep `planned_date` and `actual_date` normalized.
- Do not flatten date ranges into one date.
- Do not drop hierarchy fields just because the workbook visually hides them through merged cells.
- Do not ignore note-bearing columns just because they are not date-formatted.
- Do not convert workbook-authored status text into stronger claims than the workbook actually says.
- Do not populate `task_key` with fuzzy or weak matching output unless confidence is made explicit.

## Example Objects

### Example 1: Upcoming child milestone with parent grouping

```json
{
  "sheet": "Detailed Project schedule",
  "row": 101,
  "parent_item": "Regulatory",
  "task": "AER document submission",
  "owner": "UK PM",
  "planned_date": "2026-03-27",
  "actual_date": null,
  "date_status": "upcoming",
  "note_text": null,
  "days_to_due": 7,
  "source_signals": [
    "cell_value",
    "conditional_formatting",
    "merged_hierarchy"
  ]
}
```

### Example 2: Completed late but not explicitly blocking

```json
{
  "sheet": "Detailed Project schedule",
  "row": 19,
  "parent_item": "MD",
  "task": "Tooling launch",
  "owner": "Vendor PM",
  "planned_date": "2026-01-04",
  "actual_date": "2026-01-05",
  "note_text": null,
  "date_status": "completed_late",
  "slip_days": 1,
  "source_signals": [
    "cell_value",
    "merged_hierarchy"
  ]
}
```

### Example 3: Workbook-authored manageable delay

```json
{
  "sheet": "Detailed Project schedule",
  "row": 55,
  "parent_item": "Camera",
  "task": "Tuning review",
  "owner": "Vendor PM",
  "planned_date": "2026-04-05",
  "actual_date": null,
  "note_text": "delay but manageable",
  "note_source_column": "updated feedback",
  "date_status": "in_progress_or_delayed",
  "workbook_status": "delay_but_manageable",
  "source_signals": [
    "status_text",
    "merged_hierarchy"
  ]
}
```

## Non-Goals

This minimum schema does not yet try to cover:

- cross-workbook dependency graphs
- program-level rollups across many sheets
- automatic critical-path calculation
- full business-status ontology

Those can be added after the row-level fact object proves stable.
