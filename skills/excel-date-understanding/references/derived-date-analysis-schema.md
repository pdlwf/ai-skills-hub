# Derived Date Analysis Schema

## Purpose

This file defines the second structured output layer of the skill.

The first layer is `project_date_fact`.

The second layer is `derived_date_analysis`.

Facts describe what the workbook says after normalization.

Analysis describes what can be computed or inferred from those facts without changing the underlying workbook meaning.

## Design Principle

Prefer one row-level analysis object per milestone fact.

If needed later, workbook-level rollups can be added on top, but version 1 should stay row-first.

## Minimum Viable Object

```json
{
  "sheet": "Detailed Project schedule",
  "row": 73,
  "task": "SW boot image, power on/off animation and wallpaper release",
  "analysis_date": "2026-03-20",
  "due_soon_window_days": 14,
  "window_source": "workbook_rule",
  "derived_status": "upcoming_due_soon",
  "days_to_due": 10,
  "days_overdue": null,
  "slip_days": null,
  "analysis_signals": [
    "planned_date",
    "actual_date_blank",
    "conditional_format_due_soon",
    "note_push_out"
  ]
}
```

## Relationship To Facts

Each `derived_date_analysis` object should point back to one `project_date_fact` object through:

- `sheet`
- `row`

The analysis layer should not replace the fact layer.

It should only build on top of it.

## Required Fields

- `sheet`
  - worksheet name

- `row`
  - 1-based worksheet row number

- `task`
  - child milestone name for readability

- `analysis_date`
  - the reference date used to evaluate upcoming or overdue logic

- `due_soon_window_days`
  - integer window used to determine whether `upcoming` should be upgraded to `upcoming_due_soon`

- `window_source`
  - where the due-soon window came from
  - allowed values:
    - `workbook_rule`
    - `user_input`
    - `skill_default`

- `derived_status`
  - normalized analysis result
  - initial allowed values:
    - `done_on_time`
    - `completed_late`
    - `upcoming`
    - `upcoming_due_soon`
    - `overdue`
    - `delayed_in_progress`
    - `unresolved`

- `days_to_due`
  - integer when the task is upcoming
  - otherwise `null`

- `days_overdue`
  - integer when the task is overdue
  - otherwise `null`

- `slip_days`
  - integer when planned and actual dates are both known day-level dates and actual is later than planned
  - otherwise `null`

- `analysis_signals`
  - evidence used to derive the analysis result
  - initial allowed values:
    - `planned_date`
    - `actual_date`
    - `actual_date_blank`
    - `conditional_format_due_soon`
    - `conditional_format_delay`
    - `status_text_manageable`
    - `note_push_out`
    - `note_completion`
    - `neighboring_context`

## Recommended Fields

- `parent_item`
  - copied from the fact layer for convenience

- `owner`
  - copied from the fact layer for convenience

- `workbook_status`
  - workbook-authored status if present

- `date_range_span_days`
  - integer span for parsed date ranges

- `is_due_soon`
  - boolean

- `is_overdue`
  - boolean

- `is_completed`
  - boolean

- `is_delayed`
  - boolean

- `status_reason`
  - short explanation of why the derived status was assigned

- `anomaly_refs`
  - list of anomaly ids or references attached to the same row
  - should reference [schedule-anomaly-schema.md](schedule-anomaly-schema.md)

## Field Semantics

### `derived_status`

This field is analytical, not raw workbook content.

It should summarize the row's date posture after combining:

- normalized dates
- actual-date presence or absence
- note evidence
- conditional-format signals
- workbook-authored status text when explicit

### `days_to_due`

- compute only when:
  - planned date is a single day-level date
  - actual date is blank
  - planned date is on or after `analysis_date`

### `days_overdue`

- compute only when:
  - planned date is a single day-level date
  - actual date is blank
  - planned date is before `analysis_date`

### `slip_days`

- compute only when:
  - planned date is a single day-level date
  - actual date is a single day-level date
  - actual date is later than planned date

### `analysis_signals`

These signals explain why the analysis result exists.

They are not raw workbook values.

They are normalized reasoning traces that help keep the analysis inspectable.

### `window_source`

This field keeps due-soon analysis repeatable.

Precedence:

- workbook-defined rule
- user-specified window
- skill default

If the workbook encodes a window explicitly, prefer that over a generic default.

## Derivation Rules

- If actual date exists and actual date <= planned date:
  - `derived_status = done_on_time`

- If actual date exists and actual date > planned date:
  - `derived_status = completed_late`

- If actual date is blank and planned date is in the future:
  - `derived_status = upcoming`

- If actual date is blank and planned date is within the near-term window:
  - `derived_status = upcoming_due_soon`

- If actual date is blank and planned date is before analysis date:
  - `derived_status = overdue`

- If workbook logic explicitly indicates active delay:
  - `derived_status` may become `delayed_in_progress`

- If the row cannot be interpreted cleanly:
  - `derived_status = unresolved`

## Business Judgment Boundary

This analysis layer may say:

- `completed_late`
- `upcoming_due_soon`
- `overdue`
- `delayed_in_progress`

This analysis layer should not invent:

- `manageable`
- `blocking`

unless the workbook explicitly provides that meaning through status text or inspectable conditional-format logic.

## Stability Rules

- Always make `analysis_date` explicit.
- Always emit `due_soon_window_days` and `window_source`.
- Do not silently rely on runtime `today` without exposing that choice through these fields.

## Example Objects

### Example 1: Upcoming due soon

```json
{
  "sheet": "Detailed Project schedule",
  "row": 101,
  "task": "AER document submission",
  "analysis_date": "2026-03-20",
  "derived_status": "upcoming_due_soon",
  "days_to_due": 7,
  "days_overdue": null,
  "slip_days": null,
  "analysis_signals": [
    "planned_date",
    "actual_date_blank",
    "conditional_format_due_soon"
  ]
}
```

### Example 2: Completed late

```json
{
  "sheet": "Detailed Project schedule",
  "row": 19,
  "task": "Tooling launch",
  "analysis_date": "2026-03-20",
  "derived_status": "completed_late",
  "days_to_due": null,
  "days_overdue": null,
  "slip_days": 1,
  "analysis_signals": [
    "planned_date",
    "actual_date"
  ]
}
```

### Example 3: Delay with workbook-authored status

```json
{
  "sheet": "Detailed Project schedule",
  "row": 55,
  "task": "Tuning review",
  "analysis_date": "2026-03-20",
  "derived_status": "delayed_in_progress",
  "days_to_due": null,
  "days_overdue": null,
  "slip_days": null,
  "workbook_status": "delay_but_manageable",
  "analysis_signals": [
    "status_text_manageable",
    "conditional_format_delay"
  ]
}
```

## Non-Goals

This version does not yet define:

- workbook-level summary schemas
- cross-project rollups
- dependency-network status propagation
- critical-path computation
