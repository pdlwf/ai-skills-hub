# Schedule Anomaly Schema

## Purpose

This file defines the formal anomaly output contract for parseable but suspicious schedule values.

It standardizes the anomaly objects referenced by:

- `project_date_fact.anomaly_flags`
- `derived_date_analysis.anomaly_refs`

## Design Principle

Prefer one anomaly object per suspicious row or cell cluster.

If a single issue spans multiple cells but is caused by one coherent rule hit, emit one anomaly object with multiple references.

## Minimum Viable Object

```json
{
  "anomaly_id": "local_schedule_year_backtrack::Detailed Project schedule::D14",
  "rule_id": "local_schedule_year_backtrack_anomaly",
  "sheet": "Detailed Project schedule",
  "row": 14,
  "cell_ref": "D14",
  "severity": "high",
  "confidence": "high",
  "suspected_issue": "likely wrong year",
  "interpreted_value": "2025-01-30",
  "evidence": [
    "Previous related milestone is 2026-01-23",
    "Next related milestone is 2026-02-06",
    "The current value creates a local one-year backtrack inside one milestone sequence"
  ],
  "suggested_check": "Verify whether the intended value is 2026-01-30."
}
```

## Required Fields

- `anomaly_id`
  - stable identifier for this anomaly object

- `rule_id`
  - anomaly rule that generated the object

- `sheet`
  - worksheet name

- `row`
  - primary row reference

- `cell_ref`
  - primary cell reference or compact range reference

- `severity`
  - allowed values:
    - `low`
    - `medium`
    - `high`

- `confidence`
  - allowed values:
    - `low`
    - `medium`
    - `high`

- `suspected_issue`
  - short human-readable label

- `interpreted_value`
  - parsed value that triggered concern

- `evidence`
  - list of concrete supporting observations

- `suggested_check`
  - short user-facing verification prompt

## Recommended Fields

- `task_key`
  - stable logical task identity when available

- `task`
  - task name for readability

- `related_refs`
  - secondary rows or cells implicated in the same issue

- `warning`
  - user-facing warning text

- `business_judgment_reserved`
  - boolean
  - should usually be `true`

## Stability Rules

- Anomaly objects must reference the rule that created them.
- Anomaly objects must cite evidence, not just suspicion.
- Do not auto-correct workbook values from anomaly output alone.
- Severity and confidence are separate:
  - severity is about potential impact
  - confidence is about evidential certainty

## Business Judgment Boundary

An anomaly object may say:

- a value is suspicious
- a sequence is inconsistent
- a verification is recommended

It must not silently decide:

- manageable
- blocking
- the corrected value

unless the workbook explicitly encodes those meanings.
