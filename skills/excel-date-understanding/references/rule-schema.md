# Rule Schema

## Purpose

This file defines the standard fields for every date-understanding rule in this skill.

If a new field is added later:

- add it to this schema first
- refresh all historical rules to include it
- mark whether the field is required or optional

## Required Fields

### 1. Rule Identity

- `rule_id`
  - stable unique id
  - example: `date_range_inherit_right_side`
- `rule_name`
  - short readable name
- `rule_category`
  - example values:
    - `single_date`
    - `date_range`
    - `partial_date`
    - `date_text_extraction`
    - `excel_serial_date`
    - `date_detection`
    - `ambiguity_resolution`
    - `anomaly_detection`
    - `conditional_format_signal`
    - `scenario_comparison`
    - `state_token`
- `rule_layer`
  - required values:
    - `interpretation`
    - `anomaly`

### 2. Trigger

- `input_pattern`
  - describe what kind of input this rule applies to
- `trigger_signals`
  - concrete cues such as separators, month names, ordinal suffixes, or Excel number formats
- `preconditions`
  - assumptions required before applying the rule
- `evidence_scope`
  - define what scope the rule is allowed to inspect
  - example values:
    - `cell_only`
    - `row_context`
    - `local_sequence`
    - `sheet_context`
    - `related_tasks`
    - `conditional_formatting`

### 3. Interpretation

- `output_type`
  - example values:
    - `date`
    - `date_range`
    - `month`
    - `quarter`
    - `year`
    - `unresolved`
- `granularity`
  - example values:
    - `day`
    - `day-range`
    - `month`
    - `quarter`
    - `year`
- `normalized_value_shape`
  - define the expected normalized output structure
  - examples:
    - single date: `YYYY-MM-DD`
    - range: `{start, end}`
    - quarter: `YYYY-Qn`

### 4. Decision Logic

- `core_logic`
  - the main interpretation logic in plain language
- `inheritance_logic`
  - how omitted parts are inherited from surrounding tokens, if applicable
- `context_dependencies`
  - what context may affect interpretation, such as locale, nearby dates, column meaning, or workbook-level assumptions
- `related_task_dependencies`
  - describe how semantically related milestones or tasks may strengthen or weaken the interpretation or anomaly suspicion
- `ambiguity_policy`
  - explain when to resolve, when to warn, and when to leave unresolved

### 5. Output Metadata

- `source_evidence_policy`
  - explain which evidence sources the rule may rely on
  - example sources:
    - `cell_value`
    - `display_format`
    - `cell_text`
    - `neighboring_cells`
    - `sheet_context`
    - `conditional_formatting`
- `confidence_policy`
  - how confidence should be assigned
- `warning_policy`
  - what warning should be emitted when confidence is reduced or ambiguity exists
- `anomaly_policy`
  - explain when a value should be flagged as syntactically valid but contextually suspicious
- `user_reporting_policy`
  - explain how the rule should surface findings to the user
  - should usually include:
    - cell reference
    - current parsed value
    - why it is suspicious
    - what neighboring or related evidence supports the suspicion
    - whether final business judgment is reserved for the user

### 6. Examples

- `positive_examples`
  - inputs that should match this rule
- `expected_outputs`
  - normalized outputs for the positive examples
- `edge_cases`
  - boundary or tricky cases near this rule

## Optional Fields

- `separator_normalization`
  - use when separators vary, such as `-`, `~`, `～`, `--`
- `locale_policy`
  - use when day/month order depends on locale
- `excel_format_signals`
  - use when cell number format or display format matters
- `conditional_format_signals`
  - use when workbook conditional formatting definitions provide semantic hints such as delayed, due soon, or complete-like states
- `status_text_signals`
  - use when non-date cells contain explicit business states such as `delay but manageable`
- `write_back_policy`
  - use when the rule also governs how cleaned values should be written back to spreadsheets
- `do_not_apply_when`
  - explicit guardrails
- `notes`
  - any temporary commentary
- `anomaly_score_policy`
  - use when anomaly rules need weighted evidence instead of simple yes/no logic
- `related_task_linking_policy`
  - use when anomaly suspicion depends on inferred relationships between milestones or task sequences
- `business_judgment_boundary`
  - use when the rule may suggest severity or manageability but must preserve final user judgment
- `rule_evolution_policy`
  - use when a discovered workbook-specific pattern should be promoted into the reusable rule library after inspection

## Standard Output Object

Every interpreted date-like value should try to produce:

```json
{
  "original_value": "raw input",
  "interpreted_value": "normalized result or structured object",
  "source_layer": "cell_value | display_format | cell_text | neighboring_context | conditional_formatting",
  "output_type": "date | date_range | month | quarter | year | unresolved",
  "granularity": "day | day-range | month | quarter | year",
  "confidence": "high | medium | low",
  "anomaly_flag": false,
  "anomaly_reason": null,
  "warning": null,
  "reason": "brief explanation"
}
```

Every anomaly rule should try to produce:

```json
{
  "original_value": "2025/1/30",
  "interpreted_value": "2025-01-30",
  "source_layer": "cell_value",
  "output_type": "date",
  "granularity": "day",
  "confidence": "high",
  "anomaly_flag": true,
  "anomaly_reason": "Neighboring milestones suggest the year is likely intended to be 2026.",
  "warning": "Parsed successfully, but context indicates a likely year-entry error.",
  "reason": "The date itself is valid, but it breaks the local schedule sequence."
}
```

Recommended anomaly report object:

```json
{
  "cell": "D14",
  "parsed_value": "2025-01-30",
  "suspected_issue": "likely wrong year",
  "confidence": "high",
  "evidence": [
    "Previous related milestone is 2026-01-23",
    "Next related milestone is 2026-02-06",
    "This value creates a local year backtrack"
  ],
  "suggested_check": "Verify whether the intended value is 2026-01-30."
}
```

For ranges:

```json
{
  "original_value": "2026/7/23-30",
  "interpreted_value": {
    "start": "2026-07-23",
    "end": "2026-07-30"
  },
  "source_layer": "cell_text",
  "output_type": "date_range",
  "granularity": "day-range",
  "confidence": "high",
  "anomaly_flag": false,
  "anomaly_reason": null,
  "warning": null,
  "reason": "The right side inherits omitted year and month from the left side."
}
```

For workbook-explicit status text:

```json
{
  "cell": "F19",
  "original_value": "delay but managable",
  "interpreted_value": "delay_but_manageable",
  "source_layer": "cell_text",
  "output_type": "unresolved",
  "granularity": "day",
  "confidence": "high",
  "anomaly_flag": false,
  "anomaly_reason": null,
  "warning": null,
  "reason": "The workbook explicitly provides a business-status label in a non-date cell."
}
```

## Refresh Rule

When the schema changes:

1. update this file
2. search all historical rule documents
3. backfill missing fields
4. keep field names consistent across all rules
