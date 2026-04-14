# Cross-Scenario Comparison Schema

## Purpose

This file defines the supplemental structured output for comparing the same logical task across multiple scenario sheets.

This is not a third primary layer.

It is a comparison object built from:

- `project_date_fact`
- `derived_date_analysis`

after stable task identity has been established.

## Design Principle

Prefer one comparison object per logical task key.

Do not compare rows across sheets unless task identity is safe enough to avoid accidental merging.

## Minimum Viable Object

```json
{
  "task_key": "EVT1-8",
  "task": "二供屏 - 样品",
  "comparison_type": "planned_date_delta",
  "compared_sheets": [
    "详细计划（按1-5爬坡）挑战计划",
    "详细计划（按1-19 客户Approve）charter",
    "详细计划（1-12爬坡）如壳料无法提前风险备料则启用该计划"
  ],
  "scenario_values": {
    "详细计划（按1-5爬坡）挑战计划": {
      "planned_date": "2025-09-28",
      "actual_date": null,
      "date_status": "overdue"
    },
    "详细计划（按1-19 客户Approve）charter": {
      "planned_date": "2025-09-22",
      "actual_date": null,
      "date_status": "overdue"
    },
    "详细计划（1-12爬坡）如壳料无法提前风险备料则启用该计划": {
      "planned_date": "2025-09-22",
      "actual_date": null,
      "date_status": "overdue"
    }
  },
  "max_delta_days": 6,
  "match_confidence": "high",
  "warning": null
}
```

## Required Fields

- `task_key`
  - stable logical identity shared across compared scenario rows

- `task`
  - human-readable task name

- `comparison_type`
  - initial allowed values:
    - `planned_date_delta`
    - `actual_date_delta`
    - `status_delta`
    - `missing_in_some_scenarios`

- `compared_sheets`
  - ordered list of scenario sheet names included in the comparison

- `scenario_values`
  - per-sheet normalized values used in the comparison
  - each value object should include the relevant compared fields

- `match_confidence`
  - confidence in the identity matching across sheets
  - allowed values:
    - `high`
    - `medium`
    - `low`

- `warning`
  - comparison-specific warning or `null`

## Recommended Fields

- `task_code`
  - workbook-authored identifier if shared across sheets

- `max_delta_days`
  - maximum day difference among comparable scenario dates

- `comparison_reason`
  - short explanation of why the comparison object exists

- `missing_sheets`
  - sheets where no safe matching row was found

- `field_conflicts`
  - structured list of which fields differ

## Stability Rules

- Prefer task code over task name for identity matching.
- If only task name is available, use conservative matching and lower confidence.
- If no safe task identity exists, do not emit a comparison object.
- Treat scenario comparison as a supplemental analysis, not a correction.

## Business Judgment Boundary

This object may say that scenario timing differs.

It must not say:

- which scenario is correct
- which scenario is manageable
- which scenario is blocking

unless the workbook explicitly provides that meaning.
