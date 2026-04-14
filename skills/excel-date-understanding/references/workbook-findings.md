# Workbook Findings

## Files Reviewed

- `FRM-INV-F0003 Inventus Master File_PD1 5G Smartphone_Dec. 11th, 2025.xlsx`
- `FRM-INV-F0003 Inventus Master File_SD1 5G Tablet_Dec. 8th, 2025.xlsx`
- `P9301A项目初步计划进度表1117.xlsx`
- `P9301A项目初步计划进度表1120（内部）.xlsx`
- `X620AA项目计划进度表-硬件.xlsx`
- `T058详细计划_V1.3.xlsx`

Sheets reviewed:

- `Detailed Project schedule`
- `主计划`

## Date Format Risks Observed

### 1. Mixed true dates and text dates in the same logical date column

Observed in column `D`:

- real Excel date cells such as `2026-08-28`
- text markers such as `Done`
- text date ranges such as `2026/7/23-30`
- text date ranges crossing month boundary such as `2026/9/29~10/6`

Why this is risky:

- a generic parser may treat the column as text
- date sorting may fail
- range values need different normalization than single dates

### 2. Mixed display formats for real date cells

Observed formats:

- `mm-dd-yy`
- `yyyy/m/d;@`
- `m/d;@`

Why this is risky:

- the underlying cell value may still be a real date, but display style can suggest different parsing assumptions
- a skill must prefer the true cell value when available, not only the displayed string

### 3. Natural-language date text inside feedback cells

Examples:

- `MoU closed on 11th, Dec. 2025`
- `MoU closed on 25th, Nov. 2025`
- `Sample reached to Danny on 8th, Dec. 2025`

Why this is risky:

- the date is embedded inside explanatory text
- ordinal suffixes such as `11th` and month abbreviations such as `Dec.` need dedicated parsing logic
- the same issue can appear in any note-bearing column, not only a column literally named `feedback`

### 3b. Note-bearing columns are evidence sources, not passive comments

Observed or expected header patterns:

- `remark`
- `remarks`
- `update`
- `updates`
- `feedback`
- `updated feedback`

Why this is useful:

- these columns often contain:
  - embedded dates
  - push-out explanations
  - completion notes
  - delay-related wording
  - context that explains whether a suspicious date is actually reasonable

Why this is risky:

- a naive parser may ignore these columns because they are not date-formatted
- if they are ignored, anomaly detection loses contextual evidence and date extraction misses embedded dates

### 4. Range separators are inconsistent

Examples:

- `2026/7/23-30`
- `2026/9/29~10/6`
- `2026/7/20~24`
- `2026/10/19~21`

Why this is risky:

- a parser that only supports `-` will miss valid date ranges
- the right side may omit month and year and require inheritance from the left side

### 5. Cross-month range inheritance is required

Example:

- `2026/9/29~10/6`

Expected interpretation:

- start = `2026-09-29`
- end = `2026-10-06`

Why this is risky:

- the right side supplies month and day but omits year
- the parser must inherit the year while allowing the month to change

### 6. Formula-based date schedules are a first-class pattern

Observed in `P9301A项目初步计划进度表1117.xlsx`:

- columns `D` and `E` are heavily formula-driven
- cells are formatted as dates but store formulas such as:
  - `=E3+1`
  - `=D5+C5`
  - `=E24+1`

Why this is risky:

- reading with formula text only can make the column look non-date
- the skill must distinguish:
  - formula expression
  - cached computed date
  - displayed date format
- anomaly detection should avoid flagging normal formula-generated parallel tasks as dirty data

### 7. Non-date placeholders appear inside date-formatted cells

Observed in `X620AA项目计划进度表-硬件.xlsx`:

- `NA`
- `TBD`

Examples:

- `D10:E10`
- `D14:E14`
- `D16:E16`
- `D26:E27`
- `D30:E30`
- `D65:E65`
- `D75:E75`

Why this is risky:

- the cells are formatted as dates but do not currently contain dates
- a parser must not treat these placeholders as malformed dates
- the right interpretation is usually `unresolved schedule value`, not parse failure

### 8. Conditional formatting can encode schedule semantics

Observed in:

- `FRM-INV-F0003 Inventus Master File_PD1 5G Smartphone_Mar_18th_2026.xlsx`
- `FRM-INV-F0003 Inventus Master File_SD1 5G Tablet_Mar_18th_2026.xlsx`

Observed patterns in `Detailed Project schedule`:

- column `D` rules compare planned date vs actual date and inspect feedback text such as `delay`
- column `E` rules flag rows where planned date is within 14 days and actual date is still blank

Why this is useful:

- the workbook itself encodes business meaning beyond raw cell values
- conditional formatting can act as an extra evidence source for:
  - delay status
  - due-soon incomplete tasks
  - row-level schedule interpretation
- the same logic can be reused later as a reference pattern even in workbooks that do not define conditional formatting explicitly
- newly discovered conditional-format logic can be promoted back into the skill rule library as another reusable extraction rule

Why this is risky:

- color alone should not be trusted without reading the actual rule formula
- style may be manually overridden in some workbooks
- the skill must inspect defined conditional formatting logic, not just visible color
- conditional formatting may suggest a delay-like or attention-needed state, but it does not by itself justify stronger business judgments such as `manageable` or `blocking`

### 9. Non-date status cells can explicitly encode business judgment

Observed or expected patterns:

- `delay but manageable`
- `delay but managable`
- other nearby status phrases in remarks, owner notes, or result columns

Why this is useful:

- this is not inference; it is workbook-authored meaning
- if a non-date cell explicitly states manageability, the skill may adopt that label
- this provides a clear exception to the default rule that business-severity judgment stays with the user

Why this is risky:

- the skill should not over-normalize loose free text into stronger labels than the workbook states
- fuzzy matching must be conservative enough to catch obvious misspellings without inventing meaning

### 10. Merged cells can encode task hierarchy

Observed in:

- `FRM-INV-F0003 Inventus Master File_SD1 5G Tablet_Mar_18th_2026.xlsx`

Observed patterns in `Detailed Project schedule`:

- column `A` contains merged ranges such as:
  - `A7:A11`
  - `A13:A17`
  - `A18:A26`
  - `A27:A34`
  - `A35:A48`
  - `A49:A57`
  - `A58:A72`
  - `A73:A85`
- the merged `Item` cell acts as a parent category
- rows inside that merged block carry the detailed child milestones in column `C`

Why this is useful:

- the workbook is encoding schedule hierarchy structurally, not just visually
- each child milestone row can inherit its parent item/category even when its own `A` cell appears blank
- this makes downstream date analysis richer because each extracted milestone can retain both:
  - parent category
  - child task detail

Why this is risky:

- a naive row reader may treat blank cells inside merged ranges as missing data
- if merged hierarchy is ignored, extracted schedule facts lose grouping context
- anomaly detection and related-task reasoning become weaker when parent-child structure is dropped

### 11. One workbook can contain multiple scenario schedules for the same task set

Observed in:

- `T058详细计划_V1.3.xlsx`

Observed patterns:

- multiple sheets represent alternative schedule scenarios rather than unrelated workbooks
- examples include:
  - `详细计划（按1-5爬坡）挑战计划`
  - `详细计划（按1-19 客户Approve）charter`
  - `详细计划（1-12爬坡）如壳料无法提前风险备料则启用该计划`
- the same logical task code and task name appear across scenario sheets with different planned finish dates
- note-bearing and delay-bearing columns remain structurally similar across those sheets

Why this is useful:

- the workbook is explicitly storing schedule variants, not just one active plan
- the skill can compare the same milestone across scenarios after normalizing row-level facts
- this helps surface where timing shifts materially between plan variants

Why this is risky:

- a naive parser may treat each sheet as an isolated schedule and miss workbook-level scenario logic
- simple row-by-row extraction is not enough when the user needs to understand plan deltas
- task matching must be conservative and should prefer stable identifiers such as task code before looser name matching

### 12. Formula-driven schedule sheets may store real dates as serial-looking values under general formatting

Observed in:

- `T058详细计划_V1.3.xlsx`

Observed patterns:

- many date columns contain numeric serial values or formulas whose cached result is a numeric serial
- some relevant columns use `General` formatting rather than obvious date formatting
- examples include `开始时间`, `完成时间`, and `实际完成时间`

Why this is useful:

- the workbook still contains enough structure to recover dates from row semantics plus computed values

Why this is risky:

- strict reliance on number format will under-detect valid date columns
- the skill must use header meaning and workbook layout, not only date-like cell formatting, when deciding which numeric columns represent dates

### 13. Note-date extraction can produce false positives from part numbers, model names, and task identifiers

Observed in:

- `T058详细计划_V1.3.xlsx`

Observed patterns:

- note text contains identifiers such as:
  - `RK817-6`
  - `RK805-1`
  - task codes such as `EVT1-6`
  - version-like strings such as `V1.3`
- a loose note-date extractor may wrongly treat fragments such as `17-6` or `05-1` as month-day dates

Why this is useful:

- this workbook shows that note-bearing text can contain both real schedule dates and non-date technical identifiers in the same sentence
- a good extractor must keep embedded date support without over-capturing identifier fragments

Why this is risky:

- false-positive note dates pollute `note_dates`
- downstream analysis may incorrectly think a row contains more schedule evidence than it really does
- model names, PMIC part numbers, version tags, and task codes are common in engineering schedules, so this is a reusable protection need rather than a one-off cleanup

### 14. Ambiguous numeric dates need locale or workbook gating

Observed or expected patterns:

- `03/04/2026`
- `04/03/26`
- `20/03`

Why this is risky:

- these tokens cannot be normalized safely without locale or workbook context
- a schedule skill should expose ambiguity rather than silently choose one ordering

### 15. Excel date systems and semantic numeric date columns need explicit handling

Observed or expected patterns:

- numeric serials appear in schedule columns
- some schedule columns use `General` formatting even though the column meaning is clearly date-bearing

Why this is risky:

- numeric values may be genuine dates or ordinary quantities
- conversion should depend on workbook date system and semantic column evidence, not just numeric range checks

## Likely Data Quality Issues

These are not just format issues. They look like potential schedule-entry mistakes.

### PD1 workbook

- Cell `D14`
  - milestone: `ID confirm`
  - value: `2025/1/30`
  - risk: surrounding milestones are `2026/1/23` and `2026/2/6`, so `2025/1/30` is likely a wrong year

### SD1 workbook

- Cells `D47:D60`
  - milestones: camera temp SW version/testing sequence
  - values are in `2025`, while the preceding row `D46` is `2026/4/28`
  - risk: this looks like a year-shift error and is likely intended to be `2026`

### X620AA workbook

- Cell `E6`
  - milestone: `layout、仿真、评审`
  - cycle: `28`
  - start: `2025-12-05`
  - end: `2026-12-31`
  - risk: very likely incorrect
  - reason:
    - the stated cycle is only 28 days
    - the actual span is 392 days
    - the next nearby milestone starts on `2026-01-04`

- Cells `D12:E12`
  - milestone: `MD修改`
  - values: `2026-12-28` to `2026-12-30`
  - risk: likely incorrect
  - reason:
    - the surrounding milestone sequence is in January 2026
    - nearby rows include `D11:E11 = 2026-01-25..2026-01-28` and `D13:E13 = 2026-01-05..2026-01-12`
    - these December 2026 dates look like a local outlier inside the same schedule block

### P9301A workbook

- no strong likely-wrong date entry found yet
- main new pattern is formula-generated schedule dates rather than manual text dates

### P9301A internal workbook

- workbook: `P9301A项目初步计划进度表1120（内部）.xlsx`
- main sheet: `主计划`
- structure:
  - real Excel date cells dominate the schedule columns
  - merged cells in column `A` encode stage grouping such as `DR阶段`, `T0`, `EVT`, `DVT1`, `DVT2`, `PVT/MP`
  - notes in column `I` often contain short month/day references such as `12/5`, `1/5`, `1/21`
- useful observations:
  - the skill can recover parent grouping without relying on conditional formatting
  - row-level date analysis works well on true date cells
  - note-date extraction behaves cleanly on short human-written month/day tokens
- stability risk:
  - several rows show large differences between `周期/天` and calendar span, but the notes suggest valid schedule slack rather than bad dates
  - examples include:
    - holiday allowances such as `春节假期15天`
    - milestone buffering such as waiting for board return or parallel material prep
    - manufacturing or logistics slack such as `提前备料` or `回板`
- implication:
  - cycle-vs-span mismatch should not be treated as a strong anomaly when note text explains holidays, waiting periods, prebuild slack, or staged delivery logic

## Skill Implications

The skill should distinguish three layers:

1. `cell_value_understanding`
   - parse true Excel date values correctly
2. `text_date_extraction`
   - extract date meaning from free text such as feedback notes
3. `schedule_anomaly_detection`
   - flag values that are syntactically valid dates but contextually suspicious
4. `formula_date_resolution`
   - distinguish formula expressions from their computed date meaning
5. `placeholder_state_detection`
   - recognize `NA` and `TBD` as unresolved schedule states instead of malformed dates
6. `conditional_format_signal_extraction`
   - extract schedule meaning from workbook conditional formatting rules when present
7. `explicit_status_text_extraction`
   - extract workbook-authored business states from non-date cells when they are explicit
8. `merged_hierarchy_extraction`
   - recover parent task categories from merged cells and attach them to child milestone rows
9. `note_column_extraction`
   - extract note-bearing text from headers such as `remark`, `update`, and `feedback` as structured evidence
10. `cross_scenario_schedule_comparison`
   - compare stable task identities across multiple scenario sheets when one workbook encodes alternate plans
11. `date_field_state_token_detection`
   - distinguish `Done` or `Completed` from both real dates and unresolved placeholders
12. `schedule_slack_and_holiday_context_guard`
   - reduce anomaly confidence when note text clearly explains long spans through holidays, waiting time, staged delivery, or preparation slack

Mapped into the skill architecture:

- `interpretation rules`
  - own layers 1, 2, 4, 5, 6, 7, 8, 9, 10, and 11
- `anomaly rules`
  - own layer 3
  - may use neighboring rows, milestone sequence, and related-task linkage to raise suspicion confidence
  - may also use conditional formatting as supporting evidence or as workbook-specific logic when the formulas are inspectable
  - should report suspicious cells back to the user with explicit cell references
  - should keep final business-severity judgment with the user unless the workbook explicitly defines that meaning in status text or rule logic

## Rule Coverage Gained

These findings now justify or strengthen:

- text-embedded natural-language date interpretation
- cross-month date range inheritance
- year-backtrack anomaly detection
- related-task anomaly strengthening
- formula-based date cell resolution
- non-date placeholder detection in date-formatted cells
- cycle-vs-date-span anomaly detection
- conditional-format signal extraction
- explicit status-text extraction
- merged-cell hierarchy extraction
- note-column extraction
- cross-scenario schedule comparison
- date-field state token handling
- schedule slack and holiday context guarding
