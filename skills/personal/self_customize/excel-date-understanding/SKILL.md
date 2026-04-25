---
name: excel-date-understanding
description: Interpret messy schedule dates in spreadsheets, including hierarchy recovery, note-embedded dates, conditional formatting, and row-level date facts.
---

# Excel Date Understanding

## Use This Skill When

Use this skill when the user is working with spreadsheet schedules and needs help to:

- understand messy date columns
- normalize inconsistent date values
- parse date ranges
- extract dates from note text
- recover parent-child task hierarchy from merged cells
- interpret note columns such as `remark`, `update`, or `feedback`
- interpret conditional formatting tied to schedule status
- extract structured project-date facts
- derive row-level date analysis such as overdue, due soon, or completed late
- compare the same logical task across multiple scenario sheets
- detect suspicious but parseable schedule dates

Do not use this skill for spreadsheet work that is purely mechanical and does not depend on date semantics. Use the built-in `xlsx` skill alone for that when available.

## Dependency

This skill sits above the built-in `xlsx` skill.

- `xlsx` handles workbook I/O, formatting, formulas, merged-cell metadata, and conditional-format definitions
- this skill handles date semantics, hierarchy recovery, evidence extraction, and date analysis

## Core Workflow

1. Use the built-in `xlsx` skill to inspect workbook structure, sheet headers, cell values, formulas, merged ranges, number formats, and conditional formatting definitions.
2. Detect:
   - date-like cells
   - date-like text
   - placeholder tokens
   - state tokens in date fields
   - note-bearing columns
   - explicit status-bearing non-date text
   - merged hierarchy structure
   - stable task identity signals such as task code columns
3. Extract workbook-specific evidence:
   - conditional-format signals
   - explicit status text such as `delay but manageable`
   - note text from headers like `remark`, `update`, and `feedback`
   - parent-child task structure from merged cells
4. Run interpretation rules to normalize date values.
5. Build `project_date_fact` objects.
6. Build `derived_date_analysis` objects on top of the facts.
7. If the workbook contains scenario tabs or variant plan sheets, derive stable task identity and build cross-scenario comparison objects as supplemental analysis.
8. Run anomaly rules for suspicious but parseable dates and emit formal anomaly objects.
9. Return structured outputs first. Render prose summaries only if useful for the user.
10. If the user asks to update the workbook, use the built-in `xlsx` skill for write-back.

## Primary Outputs

This skill has two primary output layers.

### 1. Project-Date Facts

Row-level structured facts extracted from the workbook, including:

- `parent_item`
- `task`
- `owner`
- `planned_date`
- `actual_date`
- `note_text`
- `note_dates`
- `workbook_status`
- `source_signals`

Load [project-date-fact-schema.md](references/project-date-fact-schema.md) when you need the exact field contract.

### 2. Derived Date Analysis

Row-level analysis built on top of facts, including:

- `derived_status`
- `days_to_due`
- `days_overdue`
- `slip_days`
- `analysis_signals`

Load [derived-date-analysis-schema.md](references/derived-date-analysis-schema.md) when you need the exact field contract.

## Supplemental Contracts

The skill also supports two supplemental structured outputs when the workbook warrants them.

### Cross-Scenario Comparison

Use this when multiple sheets represent alternate schedules for the same logical task set.

Load [cross-scenario-comparison-schema.md](references/cross-scenario-comparison-schema.md) when you need the exact comparison contract.

### Schedule Anomaly

Use this when a date is parseable but suspicious, inconsistent, or blocked by contextual evidence.

Load [schedule-anomaly-schema.md](references/schedule-anomaly-schema.md) when you need the exact anomaly contract.

## Interpretation Rules

This skill should support:

- single-date parsing
- date-range parsing
- cross-month inheritance
- text-embedded date extraction
- guarded note-date extraction
- Excel serial date resolution
- semantic numeric date-column detection
- ambiguous numeric date locale gating
- partial date normalization
- formula-based date resolution
- placeholder detection
- date-field state token handling
- schedule slack and holiday context guarding
- explicit status-text extraction
- merged hierarchy extraction
- note-column extraction
- conditional-format signal extraction
- cross-scenario schedule comparison

Load [rule-library.md](references/rule-library.md) when you need concrete rule definitions.

Load [date-cases.md](references/date-cases.md) for example inputs and normalized outputs.

## Anomaly Rules

This skill should detect suspicious but parseable schedule values, including:

- local year backtracks
- related-task sequence inconsistencies
- cycle-vs-date-span mismatches

Use note text, merged hierarchy, and conditional-format signals to strengthen or weaken anomaly confidence.

## Evidence Rules

Treat these as part of the date-understanding surface:

- merged parent cells in grouping columns like `Item`
- note-bearing headers like `remark`, `remarks`, `update`, `updates`, `feedback`, `updated feedback`
- conditional-format formulas that encode schedule semantics
- explicit status text in non-date cells

Do not treat blank cells inside merged parent ranges as missing category data.

Do not ignore note-bearing columns just because they are not date-formatted.

## Business Judgment Boundary

This skill may infer:

- `completed_late`
- `upcoming_due_soon`
- `overdue`
- `delayed_in_progress`

This skill must not invent:

- `manageable`
- `blocking`

unless the workbook explicitly provides that meaning through:

- status text
- inspectable conditional-format logic

## Reporting Boundary

Structured outputs are primary.

Reports, summaries, and watchlists are optional renderings built on top of:

- `project_date_fact`
- `derived_date_analysis`
- cross-scenario comparison outputs
- anomaly outputs

Cross-scenario comparison is a supplemental analysis pattern built from the same facts and row-level analysis objects. It is not a third primary schema layer unless explicitly added later with approval.

## References To Load As Needed

- [workbook-findings.md](references/workbook-findings.md): known workbook patterns and risks
- [rule-library.md](references/rule-library.md): concrete rule definitions
- [rule-schema.md](references/rule-schema.md): standard rule fields and output objects
- [project-date-fact-schema.md](references/project-date-fact-schema.md): fact output contract
- [derived-date-analysis-schema.md](references/derived-date-analysis-schema.md): analysis output contract
- [cross-scenario-comparison-schema.md](references/cross-scenario-comparison-schema.md): supplemental comparison contract
- [schedule-anomaly-schema.md](references/schedule-anomaly-schema.md): anomaly output contract
- [worked-examples.md](references/worked-examples.md): real workbook examples mapped into the schemas
- [maintenance-and-learning.md](references/maintenance-and-learning.md): self-maintenance protocol
- [update-log.md](references/update-log.md): approved maintenance history

## Maintenance Rule

If you discover a reusable improvement opportunity:

1. Propose the improvement.
2. Ask for user approval before editing skill assets.
3. After approval, update the relevant files.
4. Run the local validation harness when present so schema drift and enum drift are caught before closing the update.
5. If the active workspace contains a matching repo package at `skills/excel-date-understanding`, sync the approved update back to that workspace copy when needed so the repo remains the portable source package.
6. Append an entry to [update-log.md](references/update-log.md), including which copies were updated or synchronized when relevant.

Do not silently change:

- schemas
- rule definitions
- architecture
- business-judgment boundaries

## Validation

Before trusting an interpretation:

- prefer real cell values over display text when the cell is a true Excel date
- inspect workbook date-system behavior when converting serial-like date values
- preserve date ranges instead of flattening them
- preserve merged hierarchy context
- require stable task identity before merging rows across scenario sheets
- gate ambiguous numeric dates on locale or strong workbook context
- inspect note-bearing columns for embedded dates and explanations
- inspect conditional-format formulas, not just visible color
- make `analysis_date` and due-soon window provenance explicit in derived analysis

When in doubt, prefer:

- lower confidence
- explicit warning
- unresolved output

over silent guessing

## Self Improvement

This is a `self_customize` skill. Maintain it only from the canonical folder `skills/personal/self_customize/excel-date-understanding` in the `ai-skills-hub` repo through Codex or Claude Code.

Claude App / Claude.ai uploads are read-only release snapshots. Maintain skill changes only from the canonical repo source through Codex or Claude Code.
