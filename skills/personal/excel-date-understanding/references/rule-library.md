# Rule Library

## Purpose

This file stores concrete rules using the standard schema.

## Rule 1

- `rule_id`: `date_range_cross_month_inheritance`
- `rule_name`: `Cross-Month Date Range Inheritance`
- `rule_category`: `date_range`
- `rule_layer`: `interpretation`
- `input_pattern`: date range where the left side is a fuller date and the right side omits repeated parts
- `trigger_signals`:
  - left side contains year, month, and day
  - separator is a recognized range separator
  - right side contains day only, or month and day
- `preconditions`:
  - input is in a date-like field or date-like text context
  - separator is acting as a range marker, not part of one token
- `evidence_scope`: `cell_only`
- `output_type`: `date_range`
- `granularity`: `day-range`
- `normalized_value_shape`: `{start, end}`
- `core_logic`: parse the left side as the anchor date, then inherit omitted parts on the right side while preserving any explicitly supplied right-side month or day
- `inheritance_logic`:
  - if right side only has day, inherit year and month from the left side
  - if right side has month and day, inherit year from the left side
  - do not invent missing information beyond what inheritance supports
- `context_dependencies`:
  - date-like column context can raise confidence
  - locale is low-impact when the left side is year-first and explicit
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - resolve directly when the left side is explicit enough to anchor the omitted parts
  - warn only if the right side could map to multiple valid structures
- `source_evidence_policy`:
  - primary source is `cell_text`
- `confidence_policy`:
  - `high` when left side is full and right side omission pattern is standard
  - `medium` when punctuation is noisy but still clearly range-like
- `warning_policy`:
  - no warning for clean inheritance
  - warn if the separator is nonstandard and parsing required recovery
- `anomaly_policy`:
  - not an anomaly by itself
- `user_reporting_policy`:
  - normal interpretation output only
- `separator_normalization`:
  - normalize `-`, `--`, `~`, `～`, `to` into internal `range`
- `positive_examples`:
  - `2026/7/23-30`
  - `2026/7/23～30`
  - `2026/9/29~10/6`
  - `2026/10/19~21`
- `expected_outputs`:
  - `2026/7/23-30` -> `{start: 2026-07-23, end: 2026-07-30}`
  - `2026/9/29~10/6` -> `{start: 2026-09-29, end: 2026-10-06}`
  - `2026/10/19~21` -> `{start: 2026-10-19, end: 2026-10-21}`
- `edge_cases`:
  - right side crosses year boundary such as `2026/12/29~1/3`
  - separator appears inside one malformed token
- `do_not_apply_when`:
  - neither side can be confidently recognized as date-like

Example output:

```json
{
  "original_value": "2026/9/29~10/6",
  "interpreted_value": {
    "start": "2026-09-29",
    "end": "2026-10-06"
  },
  "source_layer": "cell_text",
  "output_type": "date_range",
  "granularity": "day-range",
  "confidence": "high",
  "anomaly_flag": false,
  "anomaly_reason": null,
  "warning": null,
  "reason": "The right side explicitly supplies month and day, so the year is inherited from the left-side anchor date."
}
```

## Rule 2

- `rule_id`: `text_embedded_ordinal_month_date`
- `rule_name`: `Text-Embedded Ordinal Month Date`
- `rule_category`: `date_text_extraction`
- `rule_layer`: `interpretation`
- `input_pattern`: explanatory text that embeds a date phrase using month names and ordinal suffixes
- `trigger_signals`:
  - ordinal suffixes such as `st`, `nd`, `rd`, `th`
  - month abbreviations or month names such as `Nov.`, `Dec.`, `December`
  - surrounding free text rather than a standalone date cell
- `preconditions`:
  - a recognizable date phrase exists inside the text
- `evidence_scope`: `cell_only`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `YYYY-MM-DD`
- `core_logic`: extract the embedded date expression from the surrounding text, strip ordinal suffixes and punctuation, then normalize into a standard day-level date
- `inheritance_logic`:
  - none by default
  - if year is absent, do not auto-fill unless workbook context explicitly supports it
- `context_dependencies`:
  - month-name parsing language
  - workbook or sheet year context only if the year is omitted
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - if month name is explicit, resolve directly
  - if year is missing, lower confidence or leave unresolved depending on context strength
- `source_evidence_policy`:
  - primary source is `cell_text`
- `confidence_policy`:
  - `high` when month, day, and year are all explicit
  - `medium` when year is inferred from strong context
- `warning_policy`:
  - warn when year had to be inferred
- `anomaly_policy`:
  - not an anomaly by itself
- `user_reporting_policy`:
  - interpretation output only unless year inference was required
- `positive_examples`:
  - `MoU closed on 11th, Dec. 2025`
  - `MoU closed on 25th, Nov. 2025`
  - `Sample reached to Danny on 8th, Dec. 2025`
- `expected_outputs`:
  - `MoU closed on 11th, Dec. 2025` -> `2025-12-11`
  - `MoU closed on 25th, Nov. 2025` -> `2025-11-25`
- `edge_cases`:
  - `Mar 20th` without year
  - multilingual month text such as `2026年3月20日`

Example output:

```json
{
  "original_value": "MoU closed on 11th, Dec. 2025",
  "interpreted_value": "2025-12-11",
  "source_layer": "cell_text",
  "output_type": "date",
  "granularity": "day",
  "confidence": "high",
  "anomaly_flag": false,
  "anomaly_reason": null,
  "warning": null,
  "reason": "The text contains an explicit month name, ordinal day, and year."
}
```

## Rule 3

- `rule_id`: `local_schedule_year_backtrack_anomaly`
- `rule_name`: `Local Schedule Year Backtrack`
- `rule_category`: `anomaly_detection`
- `rule_layer`: `anomaly`
- `input_pattern`: a syntactically valid date inside a schedule sequence that unexpectedly moves backward by about one year relative to adjacent milestones
- `trigger_signals`:
  - current cell parses as a real date
  - neighboring milestones are temporally adjacent but the current row year sharply backtracks
  - the surrounding rows look like one local task sequence
- `preconditions`:
  - the inspected rows belong to the same logical schedule block or local milestone sequence
  - neighboring dates have already been interpreted
- `evidence_scope`: `local_sequence`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `YYYY-MM-DD`
- `core_logic`: accept the cell as a parseable date, then compare it against nearby schedule dates; if it causes an abrupt year backtrack that breaks local progression, flag it as suspicious
- `inheritance_logic`: not applicable
- `context_dependencies`:
  - neighboring row order
  - milestone sequence continuity
  - schedule section boundaries
- `related_task_dependencies`:
  - related milestones can strengthen suspicion if the date breaks their expected order too
- `ambiguity_policy`:
  - do not rewrite automatically
  - flag for review when contextual evidence is strong
- `source_evidence_policy`:
  - use `cell_value`, `neighboring_cells`, and `sheet_context`
- `confidence_policy`:
  - `high` when both previous and next related dates suggest the current year is inconsistent
  - `medium` when only one side supplies strong evidence
- `warning_policy`:
  - warn that the date parsed successfully but likely contains a year-entry error
- `anomaly_policy`:
  - anomaly if the date is valid in isolation but breaks local chronological consistency
- `user_reporting_policy`:
  - always report cell reference, parsed value, and evidence summary when anomaly is `medium` or `high`
  - reserve final business judgment on whether the delay is manageable for the user unless the workbook explicitly defines that status
- `anomaly_score_policy`:
  - +2 if previous related row is about one year ahead of the current value
  - +2 if next related row is about one year ahead of the current value
  - +1 if milestone names suggest the current row belongs in the same short sequence
  - anomaly threshold: 3
- `related_task_linking_policy`:
  - treat adjacent rows in one schedule subsection as related unless a new major section header starts
- `positive_examples`:
  - PD1 `D14` = `2025/1/30` between `2026/1/23` and `2026/2/6`
- `expected_outputs`:
  - flag `D14` as likely wrong-year anomaly
- `edge_cases`:
  - genuine long-cycle tasks that intentionally point to a prior year
  - reordered schedules not meant to be chronological
- `business_judgment_boundary`:
  - this rule may identify likely delay or inconsistency
  - it must not unilaterally decide whether the impact is manageable or blocking
- `do_not_apply_when`:
  - row belongs to a different section than its neighbors
  - surrounding dates are missing or themselves unresolved

Example anomaly report:

```json
{
  "cell": "D14",
  "parsed_value": "2025-01-30",
  "suspected_issue": "likely wrong year",
  "confidence": "high",
  "evidence": [
    "Previous related milestone is 2026-01-23",
    "Next related milestone is 2026-02-06",
    "The current value creates a local one-year backtrack inside one milestone sequence"
  ],
  "suggested_check": "Verify whether the intended value is 2026-01-30."
}
```

## Rule 4

- `rule_id`: `related_task_anomaly_strengthening`
- `rule_name`: `Related-Task Anomaly Strengthening`
- `rule_category`: `anomaly_detection`
- `rule_layer`: `anomaly`
- `input_pattern`: a parseable date whose anomaly confidence should rise because semantically related tasks nearby follow one coherent timeline
- `trigger_signals`:
  - repeated task family naming such as version/test/review chains
  - paired task patterns such as release -> testing, submission -> approval
  - a cluster of related tasks shares one expected project phase
- `preconditions`:
  - related-task links can be inferred with reasonable confidence
- `evidence_scope`: `related_tasks`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `YYYY-MM-DD`
- `core_logic`: do not create anomalies from semantics alone; instead, use task linkage to strengthen an existing suspicion raised by local chronology or pattern breaks
- `inheritance_logic`: not applicable
- `context_dependencies`:
  - milestone naming patterns
  - surrounding project phase structure
- `related_task_dependencies`:
  - sequence links such as `1st version -> 1st testing -> 2nd version -> 2nd testing`
  - paired deliverable and approval tasks
- `ambiguity_policy`:
  - if task linkage is weak, do not raise confidence aggressively
  - if task linkage is strong and chronology breaks, raise anomaly confidence
- `source_evidence_policy`:
  - use `cell_value`, `neighboring_cells`, and `sheet_context`
- `confidence_policy`:
  - add confidence when multiple related tasks form a coherent sequence that the current value disrupts
- `warning_policy`:
  - mention that related milestones support the anomaly suspicion
- `anomaly_policy`:
  - use as a strengthening layer, not a standalone anomaly trigger
- `user_reporting_policy`:
  - include the names of the related tasks that support the warning
  - present strengthened suspicion, but leave final business-severity judgment to the user
- `anomaly_score_policy`:
  - +1 for each strong related-task alignment signal, capped by rule design
- `related_task_linking_policy`:
  - infer links from numbering, repeated prefixes, shared workstream, and expected pairing patterns
- `positive_examples`:
  - SD1 `D47:D60` camera tuning sequence in `2025` after `D46 = 2026/4/28`
- `expected_outputs`:
  - raise anomaly confidence for the 2025 dates because the entire camera tuning chain appears to belong to the 2026 sequence
- `edge_cases`:
  - copied template phases intentionally left with placeholder years
  - related task names that are similar but actually belong to different product cycles
- `business_judgment_boundary`:
  - related-task evidence can strengthen suspicion
  - it must not by itself decide whether the delay is manageable
- `do_not_apply_when`:
  - task linkage is uncertain and chronology evidence is weak

Example anomaly report:

```json
{
  "cell_range": "D47:D60",
  "suspected_issue": "likely wrong year across related task chain",
  "confidence": "high",
  "evidence": [
    "The related camera tuning sequence begins at D46 with 2026-04-28",
    "Rows D47:D60 form one coherent version/testing chain",
    "The entire chain shifts back to 2025 while surrounding schedule context remains in 2026"
  ],
  "suggested_check": "Verify whether the dates in D47:D60 should be 2026 rather than 2025."
}
```

## Rule 5

- `rule_id`: `formula_based_date_cell_resolution`
- `rule_name`: `Formula-Based Date Cell Resolution`
- `rule_category`: `single_date`
- `rule_layer`: `interpretation`
- `input_pattern`: spreadsheet cells that are date-formatted but store formulas rather than literal date values
- `trigger_signals`:
  - cell value begins with `=`
  - cell number format is date-like
  - cached workbook value resolves to a date or date serial
- `preconditions`:
  - workbook access allows reading formula text and computed value or recalculated value
- `evidence_scope`: `cell_only`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `YYYY-MM-DD`
- `core_logic`: treat the formula as the generation mechanism, not the final date meaning; prefer the computed date result when available, while retaining the formula as provenance
- `inheritance_logic`: not applicable
- `context_dependencies`:
  - workbook recalculation state
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - if computed value is missing, report unresolved rather than pretending the formula string is a literal date
- `source_evidence_policy`:
  - use `cell_value`, `display_format`, and computed workbook value
- `confidence_policy`:
  - `high` when computed value is available and date-like
  - `medium` when formula and format strongly suggest a date but computed value is unavailable
- `warning_policy`:
  - warn if the workbook may need recalculation before trusting the computed date
- `anomaly_policy`:
  - formula presence alone is not an anomaly
- `user_reporting_policy`:
  - expose formula provenance only when useful for debugging
- `excel_format_signals`:
  - date-like formats such as `mm-dd-yy`
- `positive_examples`:
  - `P9301A!D4 = =E3+1`
  - `P9301A!E25 = =D25+C25+15`
- `expected_outputs`:
  - resolve to cached or recalculated date values instead of returning formula text
- `edge_cases`:
  - formula exists but workbook has stale or missing cached values

## Rule 6

- `rule_id`: `date_formatted_placeholder_token`
- `rule_name`: `Date-Formatted Placeholder Token`
- `rule_category`: `ambiguity_resolution`
- `rule_layer`: `interpretation`
- `input_pattern`: a date-formatted cell that contains schedule placeholder text such as `NA` or `TBD`
- `trigger_signals`:
  - cell number format is date-like
  - cell text is a known placeholder token
- `preconditions`:
  - token matches a configured placeholder vocabulary
- `evidence_scope`: `cell_only`
- `output_type`: `unresolved`
- `granularity`: `day`
- `normalized_value_shape`: `null`
- `core_logic`: classify the cell as an unresolved schedule state rather than a malformed date
- `inheritance_logic`: not applicable
- `context_dependencies`:
  - column is expected to contain dates
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - do not attempt date parsing
- `source_evidence_policy`:
  - use `cell_text` and `display_format`
- `confidence_policy`:
  - `high` when token is an exact known placeholder
- `warning_policy`:
  - optional warning that the schedule date is intentionally unresolved
- `anomaly_policy`:
  - not an anomaly by itself unless the workflow expects no unresolved dates at that stage
- `user_reporting_policy`:
  - may report as unresolved, not suspicious
- `positive_examples`:
  - `NA`
  - `TBD`
- `expected_outputs`:
  - classify as unresolved schedule value
- `edge_cases`:
  - tokens like `Done` that represent state rather than missing date

Example output:

```json
{
  "original_value": "TBD",
  "interpreted_value": null,
  "source_layer": "cell_text",
  "output_type": "unresolved",
  "granularity": "day",
  "confidence": "high",
  "anomaly_flag": false,
  "anomaly_reason": null,
  "warning": "Date field is present but the schedule value is unresolved.",
  "reason": "The cell contains a known placeholder token in a date-formatted column."
}
```

## Rule 7

- `rule_id`: `cycle_vs_date_span_anomaly`
- `rule_name`: `Cycle vs Date Span Mismatch`
- `rule_category`: `anomaly_detection`
- `rule_layer`: `anomaly`
- `input_pattern`: a task row with numeric cycle duration plus start/end dates whose actual span is wildly inconsistent with the stated cycle
- `trigger_signals`:
  - numeric duration column exists
  - start and end dates are parseable
  - actual calendar span differs materially from the declared cycle
- `preconditions`:
  - cycle column and date columns belong to the same task row
- `evidence_scope`: `row_context`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `YYYY-MM-DD`
- `core_logic`: compare the declared cycle with the actual date span; if the mismatch is extreme and unsupported by notes, flag the row as suspicious
- `inheritance_logic`: not applicable
- `context_dependencies`:
  - holiday notes may explain moderate mismatches
  - row-level task semantics may explain some slack
- `related_task_dependencies`:
  - neighboring dates can further strengthen suspicion if the row also becomes a local outlier
- `ambiguity_policy`:
  - use as anomaly evidence, not as automatic correction
- `source_evidence_policy`:
  - use `cell_value`, `neighboring_cells`, and row-level note fields
- `confidence_policy`:
  - `high` when mismatch is extreme and no explanatory note exists
  - `medium` when mismatch is large but notes could partially explain it
- `warning_policy`:
  - report that the duration and date span appear inconsistent
- `anomaly_policy`:
  - anomaly if the span difference is too large to be explained by normal scheduling slack
- `user_reporting_policy`:
  - report cell references for duration, start, and end
  - state that the row looks suspicious, but do not conclude business impact severity unless explicitly encoded
- `anomaly_score_policy`:
  - +2 when span differs from cycle by at least 180 days
  - +1 when nearby milestones indicate the row is also a chronology outlier
  - anomaly threshold: 2
- `positive_examples`:
  - `X620AA!C6=28, D6=2025-12-05, E6=2026-12-31`
- `expected_outputs`:
  - flag `E6` or the task row as likely wrong-date anomaly
- `edge_cases`:
  - notes explicitly indicate long pauses or external waiting periods
- `business_judgment_boundary`:
  - this rule can say the dates and duration look inconsistent
  - it should not conclude whether the issue is manageable without user confirmation

Example anomaly report:

```json
{
  "row": 6,
  "duration_cell": "C6",
  "start_cell": "D6",
  "end_cell": "E6",
  "suspected_issue": "cycle and date span mismatch",
  "confidence": "high",
  "evidence": [
    "Declared cycle is 28 days",
    "Actual span from 2025-12-05 to 2026-12-31 is 392 days",
    "No row note explains a year-long delay"
  ],
  "suggested_check": "Verify whether the intended end date is near early January 2026 rather than 2026-12-31."
}
```

## Rule 8

- `rule_id`: `conditional_format_signal_extraction`
- `rule_name`: `Conditional Format Signal Extraction`
- `rule_category`: `conditional_format_signal`
- `rule_layer`: `interpretation`
- `input_pattern`: workbook sheets where conditional formatting rules encode date-related schedule meaning
- `trigger_signals`:
  - conditional formatting rule formulas reference date columns
  - rule formulas inspect schedule text such as `delay`
  - rule formulas compare planned date, actual date, and blank completion state
- `preconditions`:
  - workbook conditional formatting definitions are accessible
  - rules are formula-based or otherwise inspectable
- `evidence_scope`: `conditional_formatting`
- `output_type`: `unresolved`
- `granularity`: `day`
- `normalized_value_shape`: `signal object`
- `core_logic`: inspect conditional formatting definitions and translate them into semantic schedule signals that can support interpretation and anomaly review
- `inheritance_logic`: not applicable
- `context_dependencies`:
  - sheet column meaning
  - workbook-specific business logic encoded in rule formulas
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - treat conditional formatting as workbook-specific semantic logic, not as the primary source of raw date truth
  - if rule meaning is unclear, expose the rule formula without overinterpreting it
- `source_evidence_policy`:
  - use `conditional_formatting`, `sheet_context`, and referenced cells
- `confidence_policy`:
  - `high` when rule logic is explicit and directly references date and status columns
  - `medium` when style intent is inferred but the formula is less explicit
- `warning_policy`:
  - warn if visible style could differ from defined rule intent or manual formatting may coexist
- `anomaly_policy`:
  - not an anomaly by itself
  - may strengthen anomaly suspicion when rule semantics align with other evidence
- `user_reporting_policy`:
  - report sheet, range, formula, and inferred schedule meaning
  - if the rule appears to imply a severity state, phrase it as workbook-indicated logic rather than an independent business judgment
- `conditional_format_signals`:
  - delayed
  - due soon and incomplete
  - on time or completed-like state
- `positive_examples`:
  - `AND(ISNUMBER($D7), ISNUMBER($E7), $D7<$E7, ISNUMBER(SEARCH("delay",$F7)))`
  - `AND(ISNUMBER($D7), $D7 < TODAY() + 14, ISBLANK($E7))`
- `expected_outputs`:
  - extract a signal such as `delay_status_rule`
  - extract a signal such as `due_soon_without_actual_date`
- `edge_cases`:
  - manual fill colors with no conditional formatting rule
  - rules whose style is meaningful but formula semantics are opaque
- `do_not_apply_when`:
  - workbook has no conditional formatting definitions
- `business_judgment_boundary`:
  - conditional formatting can indicate workbook-defined states such as delay-like or due-soon logic
  - unless the workbook explicitly defines manageability, the skill should not invent that label
- `rule_evolution_policy`:
  - when a new conditional-format pattern is discovered and its logic is inspectable, add it back into the rule library as another workbook-to-rule extraction pattern

Example output:

```json
{
  "sheet": "Detailed Project schedule",
  "range": "E7:E130",
  "source_layer": "conditional_formatting",
  "signal_type": "due_soon_incomplete",
  "confidence": "high",
  "rule_formula": "AND(ISNUMBER($D7), $D7 < TODAY() + 14, ISBLANK($E7))",
  "reason": "The rule marks rows where the planned date is within 14 days and the actual date is blank."
}
```

## Rule 9

- `rule_id`: `explicit_status_text_extraction`
- `rule_name`: `Explicit Status Text Extraction`
- `rule_category`: `ambiguity_resolution`
- `rule_layer`: `interpretation`
- `input_pattern`: non-date cells near a schedule row that explicitly state a business status such as `delay but manageable`
- `trigger_signals`:
  - cell text contains schedule-state keywords such as `delay`
  - cell text contains severity or impact words such as `manageable`
  - close misspellings such as `managable` still preserve obvious meaning
- `preconditions`:
  - the text is part of the workbook content, not an inferred summary generated by the agent
  - the status text is close enough to a known phrase that meaning is explicit rather than guessed
- `evidence_scope`: `row_context`
- `output_type`: `unresolved`
- `granularity`: `day`
- `normalized_value_shape`: `normalized status token`
- `core_logic`: when a nearby non-date cell explicitly states a business status, normalize that text into a controlled internal status label and treat it as workbook-authored meaning
- `inheritance_logic`: not applicable
- `context_dependencies`:
  - row-level association between the status text and the task being analyzed
  - workbook vocabulary patterns
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - accept only explicit or near-explicit phrases
  - do not infer manageability from weaker text such as `should be ok` unless the workbook repeatedly uses it as a defined status label
- `source_evidence_policy`:
  - use `cell_text`, `neighboring_cells`, and `sheet_context`
- `confidence_policy`:
  - `high` when the phrase is explicit or only contains an obvious spelling variant
  - `medium` when the phrase is shorthand but consistent with workbook vocabulary
- `warning_policy`:
  - warn if the text is fuzzy enough that normalization may collapse distinct statuses
- `anomaly_policy`:
  - not an anomaly by itself
- `user_reporting_policy`:
  - report the source cell and the normalized status
  - make clear that the status was authored by the workbook, not inferred from date logic
- `status_text_signals`:
  - `delay but manageable`
  - `delay but managable`
- `positive_examples`:
  - `delay but manageable`
  - `delay but managable`
- `expected_outputs`:
  - normalize both examples to `delay_but_manageable`
- `edge_cases`:
  - `manageable` appears alone with no delay context
  - informal text such as `delay but maybe manageable`
- `business_judgment_boundary`:
  - this rule is an exception to the default boundary because the workbook itself explicitly provides the judgment
  - the skill should still report it as workbook-authored status rather than as its own conclusion

Example output:

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
  "reason": "The workbook explicitly states a manageable delay status in a nearby non-date cell."
}
```

## Rule 10

- `rule_id`: `merged_task_hierarchy_extraction`
- `rule_name`: `Merged Task Hierarchy Extraction`
- `rule_category`: `ambiguity_resolution`
- `rule_layer`: `interpretation`
- `input_pattern`: schedule sheets where parent task categories are represented by merged cells and child milestone rows appear beneath them
- `trigger_signals`:
  - merged ranges exist in grouping columns such as `Item`
  - only the top cell of a merged range contains the visible category label
  - child rows inside the merged range contain milestone details in adjacent columns
- `preconditions`:
  - merged-cell metadata is accessible from the workbook
  - the merged range belongs to a schedule grouping column rather than decorative title cells
- `evidence_scope`: `sheet_context`
- `output_type`: `unresolved`
- `granularity`: `day`
- `normalized_value_shape`: `parent-child linkage object`
- `core_logic`: treat merged grouping cells as structural hierarchy, not visual formatting; propagate the parent category label to each child row inside the merged range so milestone facts retain their task grouping
- `inheritance_logic`:
  - inherit the merged-cell label from the top cell of the range to every row covered by that merge
  - do not inherit beyond the merged range boundary
- `context_dependencies`:
  - sheet layout
  - grouping column meaning
  - proximity of milestone detail columns
- `related_task_dependencies`:
  - parent grouping can strengthen related-task linkage and anomaly interpretation
- `ambiguity_policy`:
  - if a merge appears decorative rather than structural, do not treat it as task hierarchy automatically
- `source_evidence_policy`:
  - use `sheet_context`, merged-cell definitions, header labels, and neighboring cells
- `confidence_policy`:
  - `high` when the merged range is in a grouping column like `Item` and child rows clearly contain milestone details
  - `medium` when the hierarchy is inferred from layout but merge purpose is less explicit
- `warning_policy`:
  - warn only if the sheet uses inconsistent grouping patterns
- `anomaly_policy`:
  - not an anomaly by itself
- `user_reporting_policy`:
  - usually internal-only; expose when hierarchy materially affects date analysis output
- `positive_examples`:
  - `A73:A85` where `ROW-GMS SW` is the parent item for multiple milestone rows
  - `A18:A26` where `MD` groups several detail milestones
- `expected_outputs`:
  - child milestone rows inherit `parent_item` from the merged `Item` range
- `edge_cases`:
  - title banner merges such as `A1:B3`
  - merged cells used only for section decoration with no child task rows

Example output:

```json
{
  "row": 73,
  "parent_item": "ROW-GMS SW",
  "task": "SW boot image, power on/off animation and wallpaper release",
  "source_layer": "sheet_context",
  "reason": "The row belongs to merged Item range A73:A85, so the parent category is inherited from the top cell."
}
```

## Rule 11

- `rule_id`: `cross_scenario_schedule_comparison`
- `rule_name`: `Cross-Scenario Schedule Comparison`
- `rule_category`: `scenario_comparison`
- `rule_layer`: `interpretation`
- `input_pattern`: a workbook contains multiple scenario or variant schedule sheets that reuse the same logical task set with different planned dates
- `trigger_signals`:
  - multiple sheets share a similar schedule structure
  - task identifiers or task names recur across those sheets
  - at least one normalized date field differs across scenarios for the same logical task
- `preconditions`:
  - row-level `project_date_fact` objects have already been built for the candidate sheets
  - task matching can rely on a stable identifier such as task code, or on high-confidence task-name matching when no code exists
- `evidence_scope`: `sheet_context`
- `output_type`: `unresolved`
- `granularity`: `day`
- `normalized_value_shape`: `scenario comparison object`
- `core_logic`: group row-level schedule facts from multiple scenario sheets by logical task identity, then compare planned and actual dates across scenarios to surface meaningful deltas without changing the underlying per-sheet facts
- `inheritance_logic`: not applicable
- `context_dependencies`:
  - workbook tab naming patterns such as scenario, plan variant, challenge plan, charter, backup plan
  - shared header structure across candidate sheets
  - task-code stability across sheets
- `related_task_dependencies`:
  - related-task linkage can help only after primary task identity is established
- `ambiguity_policy`:
  - prefer task code or other stable identifiers over task-name-only matching
  - if matching confidence is weak, do not merge tasks across sheets
  - report the comparison as supplemental analysis, not as a replacement for row-level facts
- `source_evidence_policy`:
  - use normalized `project_date_fact` objects, sheet names, task identifiers, and row-level date fields
- `confidence_policy`:
  - `high` when task code and task name both align across scenario sheets
  - `medium` when task name aligns strongly but identifiers are missing
- `warning_policy`:
  - warn when task matching required fuzzy name alignment or when one scenario is missing a corresponding task row
- `anomaly_policy`:
  - scenario differences are not anomalies by themselves
  - large deltas may later strengthen anomaly review when combined with other evidence
- `user_reporting_policy`:
  - report the logical task identifier, the participating sheets, and the date deltas
  - describe the result as a scenario difference, not as a schedule error
- `comparison_fields`:
  - `planned_date`
  - `actual_date`
  - `date_status`
  - `days_overdue`
  - `days_to_due`
- `matching_policy`:
  - primary key: stable task code column when present
  - fallback key: normalized task name with conservative matching
  - do not merge rows across sheets when both keys are weak
- `positive_examples`:
  - `T058详细计划_V1.3.xlsx`
  - `EVT1-8 / 二供屏 - 样品`
  - `EVT1-25 / 第一版用户软件释放`
- `expected_outputs`:
  - detect that one task has different planned finish dates across `挑战计划`, `charter`, and backup-plan sheets
  - preserve each per-sheet fact while additionally exposing the delta object
- `edge_cases`:
  - one scenario sheet intentionally omits tasks that do not apply
  - the same task name is reused for different project phases
  - scenario tabs have diverged structure and only partial task overlap
- `business_judgment_boundary`:
  - this rule may say that scenarios differ in schedule timing
  - it must not claim which scenario is correct or more manageable unless the workbook explicitly says so

Example output:

```json
{
  "task_key": "EVT1-8",
  "task": "二供屏 - 样品",
  "comparison_type": "planned_date_delta",
  "scenarios": {
    "详细计划（按1-5爬坡）挑战计划": "2025-09-28",
    "详细计划（按1-19 客户Approve）charter": "2025-09-22",
    "详细计划（1-12爬坡）如壳料无法提前风险备料则启用该计划": "2025-09-22"
  },
  "max_delta_days": 6,
  "confidence": "high",
  "reason": "The same logical task appears across multiple scenario sheets with matching identifiers but different planned finish dates."
}
```

## Rule 12

- `rule_id`: `note_date_false_positive_guard`
- `rule_name`: `Note-Date False Positive Guard`
- `rule_category`: `date_text_extraction`
- `rule_layer`: `interpretation`
- `input_pattern`: note-bearing text contains both real schedule dates and non-date technical identifiers that resemble short date tokens
- `trigger_signals`:
  - note text includes slash or dash separated numeric fragments
  - nearby text also includes letter-digit or model-like identifiers
  - extracted candidate date token is only weakly date-like in context
- `preconditions`:
  - note-date extraction is being applied to free text from columns such as `remark`, `update`, `feedback`, `备注`, `风险`, or `delay 描述`
- `evidence_scope`: `cell_only`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `filtered date candidate list`
- `core_logic`: treat note-date extraction as a guarded pass; keep candidates that read like human schedule expressions and suppress candidates that are more plausibly part numbers, model names, version tags, or task identifiers
- `inheritance_logic`:
  - none by default
- `context_dependencies`:
  - token boundaries
  - adjacent alphabetic characters
  - workbook vocabulary patterns such as chip names, part numbers, task codes, and version labels
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - when a candidate token is equally plausible as a date and as an identifier fragment, prefer suppression or low confidence
  - keep candidates when surrounding text clearly frames them as time, such as `推至8/5`, `时间7/17`, `from 3/20`, or `on 11th, Dec. 2025`
- `source_evidence_policy`:
  - use `cell_text` plus local token context
- `confidence_policy`:
  - `high` when the token is framed by clear temporal language or a standard date separator pattern with clean boundaries
  - `medium` when the token is date-like but lacks surrounding time language
  - `low` when the token is embedded inside a model or identifier context
- `warning_policy`:
  - optional warning when note text contains mixed date-like and identifier-like patterns and only some candidates were kept
- `anomaly_policy`:
  - not an anomaly by itself
- `user_reporting_policy`:
  - usually internal-only
  - expose only when explaining why some date-like fragments were intentionally ignored
- `suppression_signals`:
  - alphabetic prefix directly attached to the token
  - token sits inside a longer identifier such as `RK817-6`, `EVT1-6`, or `V1.3`
  - candidate month or day would be implausible without special context
- `keep_signals`:
  - preceding words such as `时间`, `推至`, `改到`, `from`, `to`, `on`, `by`
  - whitespace or punctuation boundaries around the token
  - presence of year-first or standard month/day formatting
- `positive_examples`:
  - keep `7/17` in `计划投模时间7/17`
  - keep `8/5` in `投模时间调整为8/5`
  - suppress `17-6` in `RK817-6`
  - suppress `05-1` in `RK805-1`
  - suppress `1-6` in `EVT1-6`
- `expected_outputs`:
  - note-date extraction retains real schedule dates while excluding identifier fragments that only superficially resemble dates
- `edge_cases`:
  - identifiers separated by spaces that still look date-like
  - multilingual note text mixing Chinese schedule language and English part numbers
- `business_judgment_boundary`:
  - this rule only improves extraction quality
  - it does not change any downstream business-status judgment

Example output:

```json
{
  "cell": "H4",
  "original_value": "原理图时间推后1天：PMU由RK817-6改为RK805-1",
  "kept_note_dates": [],
  "suppressed_candidates": ["17-6", "05-1"],
  "source_layer": "cell_text",
  "reason": "The candidate tokens appear inside PMIC model identifiers rather than human-readable schedule expressions."
}
```

## Rule 18

- `rule_id`: `dependency_conflict_from_conditional_format`
- `rule_name`: `Dependency Conflict From Conditional Format`
- `rule_category`: `anomaly_detection`
- `rule_layer`: `anomaly`
- `input_pattern`: a workbook conditional-format rule or equivalent row logic indicates that a task starts before a declared dependency finishes
- `trigger_signals`:
  - row has a dependency reference
  - planned start implied by row dates and cycle occurs before dependency completion
  - workbook conditional-format logic flags the relationship or encodes the same comparison
- `preconditions`:
  - dependency identity can be resolved to another task row
  - date-bearing columns for the row and dependency are parseable
- `evidence_scope`: `row_context`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `YYYY-MM-DD`
- `core_logic`: use dependency linkage plus workbook rule logic to detect when a task is scheduled to begin before its prerequisite task is planned to complete
- `inheritance_logic`:
  - not applicable
- `context_dependencies`:
  - dependency column semantics
  - workbook formula or conditional-format logic
- `related_task_dependencies`:
  - dependency row is required supporting evidence
- `ambiguity_policy`:
  - if dependency resolution is weak, do not emit the anomaly
- `source_evidence_policy`:
  - use `cell_value`, `neighboring_cells`, and `conditional_formatting`
- `confidence_policy`:
  - `high` when workbook logic explicitly encodes the dependency check
  - `medium` when the same conflict is inferred from row arithmetic without an explicit workbook rule
- `warning_policy`:
  - warn that the current row appears to start before its dependency completes
- `anomaly_policy`:
  - anomaly when dependency chronology is violated
- `user_reporting_policy`:
  - report the current row, dependency row, and the conflicting dates
- `positive_examples`:
  - `T058详细计划_V1.3.xlsx` backup plan row `MP-2`
- `expected_outputs`:
  - flag the row as a dependency schedule conflict
- `edge_cases`:
  - dependencies that intentionally overlap
  - dependency columns that refer to milestone groups rather than one row

## Rule 19

- `rule_id`: `schedule_slack_and_holiday_context_guard`
- `rule_name`: `Schedule Slack And Holiday Context Guard`
- `rule_category`: `anomaly_detection`
- `rule_layer`: `anomaly`
- `input_pattern`: a row looks anomalous based on cycle-vs-span or lateness checks, but note text explicitly explains non-error schedule slack
- `trigger_signals`:
  - row has note-bearing text
  - notes mention holidays, waiting periods, buffering, prebuild preparation, phased delivery, or similar schedule explanations
  - another anomaly rule would otherwise raise or strengthen suspicion
- `preconditions`:
  - note text is clearly associated with the same task row
- `evidence_scope`: `row_context`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `guarded anomaly decision`
- `core_logic`: use explanatory note text to weaken or suppress anomaly confidence when the date span is plausibly explained by normal project slack rather than a likely bad date entry
- `inheritance_logic`:
  - not applicable
- `context_dependencies`:
  - note-bearing columns
  - row-level cycle and span values
  - workbook-specific scheduling habits
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - only lower anomaly confidence when the note text gives a concrete temporal explanation
  - do not suppress anomalies just because a note exists; the note must plausibly explain the span or delay
- `source_evidence_policy`:
  - use `cell_text`, row-level dates, cycle values, and anomaly context from the triggering rule
- `confidence_policy`:
  - reduce anomaly confidence by one level when note evidence is moderately explanatory
  - suppress anomaly escalation when note evidence is strong and directly explains the slack
- `warning_policy`:
  - report that the row contains schedule slack context and may not represent a bad date entry
- `anomaly_policy`:
  - this rule does not create anomalies
  - it only weakens or suppresses anomaly suspicion raised elsewhere
- `user_reporting_policy`:
  - if used, explain which note phrase reduced anomaly confidence
- `positive_examples`:
  - `春节假期15天`
  - `五一假期3天`
  - `提前备料`
  - `回板`
  - `先交1k，一周后再交剩余4k`
- `expected_outputs`:
  - lower confidence for cycle-vs-span mismatch when holiday or staged-delivery notes plausibly explain the difference
- `edge_cases`:
  - vague notes that do not actually explain the span
  - notes copied from nearby rows that do not belong to the current task

Example output:

```json
{
  "row": 29,
  "task": "V1.0 驱动调试",
  "guard_type": "holiday_or_schedule_slack",
  "affected_rule": "cycle_vs_date_span_anomaly",
  "confidence_adjustment": "down",
  "reason": "The note mentions 春节假期15天, which plausibly explains part of the long calendar span."
}
```

## Rule 13

- `rule_id`: `excel_serial_date_resolution`
- `rule_name`: `Excel Serial Date Resolution`
- `rule_category`: `excel_serial_date`
- `rule_layer`: `interpretation`
- `input_pattern`: a numeric cell in a date-like schedule column may represent an Excel serial date
- `trigger_signals`:
  - cell value is numeric
  - header or nearby column meaning is date-like
  - workbook structure suggests schedule dates rather than plain quantities
- `preconditions`:
  - workbook date system is known or can be detected
- `evidence_scope`: `cell_only`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `YYYY-MM-DD`
- `core_logic`: convert numeric Excel serials to real dates only when workbook semantics or cell formatting provide enough evidence that the column is date-bearing
- `inheritance_logic`:
  - not applicable
- `context_dependencies`:
  - workbook date system
  - date-like headers
  - neighboring date patterns
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - if the value is numeric but the column meaning is unclear, leave unresolved rather than silently coercing it to a date
- `source_evidence_policy`:
  - use `cell_value`, `display_format`, and `sheet_context`
- `confidence_policy`:
  - `high` when both the value and column semantics indicate a date
  - `medium` when only one strong signal exists
- `warning_policy`:
  - warn when conversion relied on semantic column detection rather than explicit date formatting
- `anomaly_policy`:
  - serial conversion alone is not an anomaly
- `user_reporting_policy`:
  - expose workbook date-system assumptions when they materially affect the result
- `positive_examples`:
  - `45834` in a `开始时间` column
  - `45849` in a `完成时间` column
- `expected_outputs`:
  - convert serial values to normalized day-level dates when evidence is sufficient
- `edge_cases`:
  - quantity columns containing numbers that happen to fall into Excel serial ranges
  - stale computed values in formula-driven sheets

## Rule 14

- `rule_id`: `header_semantic_numeric_date_detection`
- `rule_name`: `Header-Semantic Numeric Date Detection`
- `rule_category`: `date_detection`
- `rule_layer`: `interpretation`
- `input_pattern`: date columns are not explicitly date-formatted, but sheet headers and row layout indicate that numeric values represent dates
- `trigger_signals`:
  - headers such as `开始时间`, `完成时间`, `实际完成时间`, `schedule`, `ETA`
  - neighboring columns form a start/end/actual pattern
  - values align with date-like progression rather than arbitrary quantities
- `preconditions`:
  - the sheet has enough structural context to infer column meaning
- `evidence_scope`: `sheet_context`
- `output_type`: `date`
- `granularity`: `day`
- `normalized_value_shape`: `date-bearing column detection`
- `core_logic`: use header semantics and repeated row structure to decide whether a numeric column should be treated as date-bearing even if number format is general
- `inheritance_logic`:
  - not applicable
- `context_dependencies`:
  - header row quality
  - neighboring date columns
  - formula relationships across rows
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - require multiple structural clues before upgrading a general-formatted numeric column to date-bearing
- `source_evidence_policy`:
  - use `sheet_context`, headers, formulas, and neighboring cells
- `confidence_policy`:
  - `high` when the column participates in a repeated schedule pattern
  - `medium` when header semantics are strong but row structure is noisy
- `warning_policy`:
  - warn when date-bearing detection is semantic rather than explicit
- `anomaly_policy`:
  - not an anomaly by itself
- `user_reporting_policy`:
  - internal by default
- `positive_examples`:
  - `T058详细计划_V1.3.xlsx` columns `开始时间` / `完成时间` stored as numeric serials under general formatting
- `expected_outputs`:
  - mark the column as date-bearing so serial resolution can proceed safely
- `edge_cases`:
  - summary tables that reuse schedule-like headers for non-date metrics

## Rule 15

- `rule_id`: `ambiguous_numeric_date_locale_gate`
- `rule_name`: `Ambiguous Numeric Date Locale Gate`
- `rule_category`: `ambiguity_resolution`
- `rule_layer`: `interpretation`
- `input_pattern`: slash- or dash-separated numeric text where day-month order is ambiguous
- `trigger_signals`:
  - values such as `03/04/2026`, `04/03/26`, `20/03`
  - no explicit month name
  - no year-first ordering
- `preconditions`:
  - the token is being interpreted as a date candidate
- `evidence_scope`: `cell_only`
- `output_type`: `unresolved`
- `granularity`: `day`
- `normalized_value_shape`: `null or gated date candidate`
- `core_logic`: do not normalize ambiguous numeric dates unless locale or workbook context clearly resolves the order
- `inheritance_logic`:
  - none by default
- `context_dependencies`:
  - locale
  - workbook conventions
  - neighboring explicit dates
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - if locale is unknown and context is weak, leave unresolved and emit a warning
- `source_evidence_policy`:
  - use `cell_text`, `sheet_context`, and neighboring explicit dates
- `confidence_policy`:
  - `high` only when locale or workbook pattern is explicit
  - `low` when interpretation would otherwise be a guess
- `warning_policy`:
  - warn that the token is ambiguous without locale or workbook context
- `anomaly_policy`:
  - ambiguity is not an anomaly
- `user_reporting_policy`:
  - make the ambiguity explicit rather than hiding it
- `positive_examples`:
  - `03/04/2026`
  - `04/03/26`
  - `20/03`
- `expected_outputs`:
  - unresolved unless locale or workbook pattern safely resolves the order
- `edge_cases`:
  - workbooks that mix locales across sheets

## Rule 16

- `rule_id`: `partial_date_normalization`
- `rule_name`: `Partial Date Normalization`
- `rule_category`: `partial_date`
- `rule_layer`: `interpretation`
- `input_pattern`: date text expresses only part of a calendar date such as month-day, month, quarter, or year
- `trigger_signals`:
  - values such as `Mar 20th`, `20/03`, `Q3 2026`, `2026年3月`
  - missing explicit year, day, or both
- `preconditions`:
  - the token is clearly date-like but incomplete
- `evidence_scope`: `cell_only`
- `output_type`: `month`
- `granularity`: `month`
- `normalized_value_shape`: `partial date object`
- `core_logic`: preserve partial date meaning without overfilling missing parts unless workbook context explicitly supports inheritance
- `inheritance_logic`:
  - allow year inheritance only from strong workbook or sheet context
  - do not invent a missing day without explicit support
- `context_dependencies`:
  - workbook year context
  - surrounding date range
  - locale
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - preserve the highest-confidence partial representation rather than forcing a full day-level date
- `source_evidence_policy`:
  - use `cell_text`, `sheet_context`, and neighboring explicit dates
- `confidence_policy`:
  - `high` when the expressed granularity is explicit
  - `medium` when year is inherited from strong context
- `warning_policy`:
  - warn when inherited context fills a missing year
- `anomaly_policy`:
  - partial dates are not anomalies by themselves
- `user_reporting_policy`:
  - expose the preserved granularity
- `positive_examples`:
  - `Mar 20th`
  - `2026年3月`
  - `Q3 2026`
- `expected_outputs`:
  - preserve partial granularity instead of forcing a full `YYYY-MM-DD`
- `edge_cases`:
  - month-day values that are also locale-ambiguous numeric tokens

## Rule 17

- `rule_id`: `date_field_state_token`
- `rule_name`: `Date-Field State Token`
- `rule_category`: `state_token`
- `rule_layer`: `interpretation`
- `input_pattern`: a logical date field contains a workbook state token such as `Done` or `Completed` instead of a date
- `trigger_signals`:
  - cell text matches a known completion-state vocabulary
  - the column is otherwise date-bearing
- `preconditions`:
  - token is workbook-authored state, not freeform note text
- `evidence_scope`: `cell_only`
- `output_type`: `unresolved`
- `granularity`: `day`
- `normalized_value_shape`: `state token object`
- `core_logic`: classify the token as a completion-state signal in a date field, distinct from unresolved placeholders and distinct from a real parsed date
- `inheritance_logic`:
  - not applicable
- `context_dependencies`:
  - whether an actual date exists elsewhere on the row
  - workbook conventions for completion fields
- `related_task_dependencies`: none required
- `ambiguity_policy`:
  - do not convert `Done` into a date
  - use row context to decide whether the row should remain unresolved or infer completion state separately
- `source_evidence_policy`:
  - use `cell_text`, `sheet_context`, and neighboring cells
- `confidence_policy`:
  - `high` when token matches workbook vocabulary exactly
- `warning_policy`:
  - optional warning that the date field stores a state token rather than a date
- `anomaly_policy`:
  - not an anomaly by itself
- `user_reporting_policy`:
  - report as a field-state interpretation, not as malformed data
- `positive_examples`:
  - `Done`
  - `Completed`
- `expected_outputs`:
  - keep the row interpretable without pretending the token is a date or a missing value token
- `edge_cases`:
  - `Done 12/3` where one token mixes state and date
  - workbooks that use `Done` as a separate status column rather than in a date field
