# Update Log

## Purpose

This file records approved maintenance updates to the skill design.

Only write an entry after the update is approved and applied.

## Entry Template

```markdown
### YYYY-MM-DD - Short Update Title

- Trigger:
  - what new workbook pattern, user correction, or capability gap caused the update
- Approved by user:
  - yes
- Changes:
  - short list of what was added, revised, or clarified
- Files updated:
  - path list
- Capability gained:
  - what the skill can now do better
- Notes:
  - optional boundary or caveat
```

## Entries

### 2026-04-09 - Added Holiday And Slack Guard For Span Anomalies

- Trigger:
  - user provided `P9301A项目初步计划进度表1120（内部）.xlsx` as test data, which showed that several cycle-vs-span mismatches were plausibly explained by holidays or schedule slack rather than bad date entries
- Approved by user:
  - yes
- Changes:
  - added a guard rule to reduce anomaly confidence when note text clearly explains long spans through holidays, waiting time, staging, or preparation slack
  - documented the internal P9301A workbook pattern in workbook findings
  - added a worked example showing anomaly-confidence reduction rather than escalation
- Files updated:
  - `skills/excel-date-understanding/SKILL.md`
  - `skills/excel-date-understanding/references/rule-library.md`
  - `skills/excel-date-understanding/references/workbook-findings.md`
  - `skills/excel-date-understanding/references/worked-examples.md`
  - `skills/excel-date-understanding/references/update-log.md`
- Capability gained:
  - the skill is less likely to over-flag cycle-vs-span mismatches when workbook notes provide a concrete temporal explanation
- Notes:
  - this guard weakens anomaly confidence only when note evidence is specific enough to explain the extra span

### 2026-04-09 - Stability Contracts And Validation Hardening

- Trigger:
  - user requested a deeper stability review of the skill and approved a hardening pass after independent review identified schema drift, missing contracts, and rule gaps
- Approved by user:
  - yes
- Changes:
  - aligned the packaged `SKILL.md`, schemas, maintenance flow, and worked examples around the same current contract
  - added stable task-identity support to `project_date_fact`
  - added formal supplemental contracts for cross-scenario comparison and schedule anomalies
  - added missing rules for Excel serial resolution, semantic numeric date detection, ambiguous numeric date gating, partial date normalization, date-field state tokens, and dependency conflicts
  - added a validation harness to catch schema drift and enum drift
- Files updated:
  - `skills/excel-date-understanding/SKILL.md`
  - `skills/excel-date-understanding/references/project-date-fact-schema.md`
  - `skills/excel-date-understanding/references/derived-date-analysis-schema.md`
  - `skills/excel-date-understanding/references/rule-schema.md`
  - `skills/excel-date-understanding/references/rule-library.md`
  - `skills/excel-date-understanding/references/workbook-findings.md`
  - `skills/excel-date-understanding/references/worked-examples.md`
  - `skills/excel-date-understanding/references/maintenance-and-learning.md`
  - `skills/excel-date-understanding/references/cross-scenario-comparison-schema.md`
  - `skills/excel-date-understanding/references/schedule-anomaly-schema.md`
  - `skills/excel-date-understanding/references/update-log.md`
  - `skills/excel-date-understanding/scripts/validate_skill.py`
- Capability gained:
  - the skill now has stronger identity handling, formal anomaly and scenario-comparison contracts, broader date coverage, and a repeatable local validation path
- Notes:
  - this hardening pass keeps the existing two primary output layers while adding supplemental contracts for comparison and anomaly outputs
  - workspace portable package and installed copy should be synchronized together after approved updates

### 2026-03-20 - Added Repo Sync-Back Policy

- Trigger:
  - user asked that future approved updates made while using the installed skill in other conversations should be able to sync back into the current repo package
- Approved by user:
  - yes
- Changes:
  - added a maintenance rule that treats `skills/excel-date-understanding` in the active workspace as the portable repo package when present
  - required approved changes to sync back to that workspace package when the skill is being maintained from an installed copy
  - clarified that update logs should record which copies were synchronized
- Files updated:
  - `skills/excel-date-understanding/SKILL.md`
  - `skills/excel-date-understanding/references/maintenance-and-learning.md`
  - `skills/excel-date-understanding/references/update-log.md`
- Capability gained:
  - future approved skill changes made in other conversations can be synchronized back into the repo package instead of only living in the installed copy
- Notes:
  - this policy only applies after user approval for the underlying skill change; it does not authorize silent behavior edits

### 2026-03-20 - Added Note-Date False Positive Guard

- Trigger:
  - workbook analysis showed that note extraction could misread model numbers, version-like strings, and task identifiers as short dates
- Approved by user:
  - yes
- Changes:
  - added a guarded note-date extraction rule to suppress false positives from part numbers, model names, and task codes
  - updated the packaged `SKILL.md` to explicitly support guarded note-date extraction
  - added workbook findings documenting this reusable failure mode
- Files updated:
  - `skills/excel-date-understanding/SKILL.md`
  - `skills/excel-date-understanding/references/rule-library.md`
  - `skills/excel-date-understanding/references/workbook-findings.md`
  - `skills/excel-date-understanding/references/update-log.md`
- Capability gained:
  - the skill can now keep real embedded schedule dates in note text while avoiding common false positives from engineering identifiers
- Notes:
  - this update improves extraction quality only; it does not change status or business-judgment boundaries

### 2026-03-20 - Added Cross-Scenario Schedule Comparison

- Trigger:
  - analysis of `T058详细计划_V1.3.xlsx` showed that one workbook can contain multiple scenario tabs with the same logical task set but different planned dates
- Approved by user:
  - yes
- Changes:
  - added a reusable rule for comparing the same logical task across scenario sheets
  - updated the packaged `SKILL.md` to treat cross-scenario comparison as a supported supplemental analysis pattern
  - added workbook findings about multi-scenario schedule packages and general-formatted serial date columns
- Files updated:
  - `skills/excel-date-understanding/SKILL.md`
  - `skills/excel-date-understanding/references/rule-library.md`
  - `skills/excel-date-understanding/references/workbook-findings.md`
  - `skills/excel-date-understanding/references/update-log.md`
- Capability gained:
  - the skill can now compare normalized dates for the same task across multiple scenario sheets without breaking the existing two-layer fact/analysis design
- Notes:
  - this update does not yet add a new primary schema layer; cross-scenario output remains supplemental analysis built from row-level facts

### 2026-03-20 - Added Agent Metadata

- Trigger:
  - user approved making the portable skill package closer to a formally installable skill
- Approved by user:
  - yes
- Changes:
  - added `agents/openai.yaml` for UI-facing skill metadata
  - defined display name, short description, and default prompt for the packaged skill
- Files updated:
  - `skills/excel-date-understanding/agents/openai.yaml`
  - `skills/excel-date-understanding/references/update-log.md`
- Capability gained:
  - the packaged skill now has explicit agent metadata for skill lists and prompt insertion
- Notes:
  - icon assets were intentionally omitted for now

### 2026-03-20 - Portable Skill Package Created

- Trigger:
  - user requested a self-contained skill folder inside the repo so the skill can be moved to another computer without breaking file references
- Approved by user:
  - yes
- Changes:
  - created a portable skill package under `skills/excel-date-understanding`
  - copied the referenced design assets into the package `references/` directory
  - rewrote the packaged `SKILL.md` to use only internal relative references instead of machine-specific absolute paths
- Files updated:
  - `skills/excel-date-understanding/SKILL.md`
  - `skills/excel-date-understanding/references/*`
- Capability gained:
  - the skill can now be moved and installed on another machine without losing its internal reference files
- Notes:
  - dependency on the built-in `xlsx` skill remains conceptual, but no external file paths are required by this package

### 2026-03-20 - Initial SKILL.md Draft Added

- Trigger:
  - user approved moving from design artifacts into a formal skill draft
- Approved by user:
  - yes
- Changes:
  - added a formal `SKILL.md` with trigger conditions, workflow, output layers, boundaries, references, and maintenance rules
  - linked the formal skill draft from the idea README
- Files updated:
  - `SKILL.md`
  - `README.md`
- Capability gained:
  - the idea now has an executable skill draft shape rather than only supporting design documents
- Notes:
  - this is still a draft and can continue to evolve under the approval-before-optimization rule

### 2026-03-20 - Self-Maintenance Governance Added

- Trigger:
  - user asked the skill to be self-maintaining, to keep a record of each update, and to always ask for approval before optimization
- Approved by user:
  - yes
- Changes:
  - added a maintenance-and-learning protocol
  - established approval-before-optimization as a hard rule
  - created a dedicated update log for future approved changes
- Files updated:
  - `13-maintenance-and-learning.md`
  - `14-update-log.md`
  - `02-pd.md`
  - `08-skill-architecture.md`
  - `09-skill-draft.md`
  - `README.md`
- Capability gained:
  - the skill now has an explicit lifecycle for proposing, approving, applying, and recording improvements
- Notes:
  - future behavior upgrades should be proposed first and only applied after user approval
