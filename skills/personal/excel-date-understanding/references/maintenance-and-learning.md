# Maintenance And Learning

## Purpose

This file defines how the skill should improve over time.

The goal is not only to make one useful skill.

The goal is to make one skill that can:

- learn from repeated real workbook usage
- absorb new techniques you teach during later conversations
- propose structured improvements instead of forgetting them
- record every approved update so the skill keeps getting stronger

## Core Principle

The skill may discover improvement opportunities by itself, but it must not silently update its own design or behavior contract.

It must first ask for your approval.

## Learning Sources

The skill should learn from:

- new workbook patterns found during real usage
- new date formats or malformed formats you explain
- new merged-structure patterns
- new note-column behaviors
- new conditional-format rules
- new business-status phrases
- your explicit corrections
- your preferred interpretation boundaries

## Improvement Loop

Every time the skill notices a new reusable pattern, it should follow this loop:

1. Detect
   - identify the new pattern, gap, or failure mode

2. Propose
   - explain what new capability or rule should be added
   - explain why it is reusable beyond one workbook

3. Ask Approval
   - ask your permission before changing the skill design artifacts
   - no silent schema edits
   - no silent rule-library edits
   - no silent maintenance-log edits that imply behavior changes

4. Apply
   - once approved, update the relevant design files

5. Validate
   - run `scripts/validate_skill.py` when present
   - do not treat an update as complete if the validation harness reports schema drift or enum drift

6. Sync Back To Repo Package
   - if the skill is being used from an installed copy and the active workspace contains `skills/excel-date-understanding`
   - treat that workspace copy as the portable repo package
   - sync the approved changes back to that repo package as part of the same maintenance action
   - if both installed copy and workspace copy are updated, verify both sides rather than assuming they match

7. Record
   - append one maintenance entry to `references/update-log.md`
   - summarize:
     - what changed
     - why it changed
     - which files were updated
     - which copies were synchronized
     - what new capability was gained

## Approval Boundary

The skill may do these without asking:

- analyze a workbook using existing approved logic
- point out likely future improvements
- draft a proposed update for review

The skill must ask before doing these:

- changing rule definitions
- changing schema definitions
- changing maintenance policy
- changing skill architecture
- promoting a one-off pattern into reusable skill behavior
- revising the interpretation boundary for business judgment
- changing repo-sync behavior for installed vs workspace copies

## What Counts As A Reusable Improvement

Examples:

- adding support for a new range separator
- adding a new note-column header pattern
- adding a new conditional-format extraction rule
- adding a new merged hierarchy pattern
- refining a date anomaly rule based on repeated workbook evidence

Non-examples:

- describing one workbook row without changing skill behavior
- producing one temporary analysis result

## Update Targets

When an approved improvement is applied, update only the files that actually need it.

Typical targets:

- `SKILL.md`
- `references/rule-schema.md`
- `references/workbook-findings.md`
- `references/rule-library.md`
- `references/project-date-fact-schema.md`
- `references/derived-date-analysis-schema.md`
- `references/cross-scenario-comparison-schema.md`
- `references/schedule-anomaly-schema.md`
- `references/worked-examples.md`
- `references/maintenance-and-learning.md`
- `references/update-log.md`
- `scripts/validate_skill.py`

When the skill exists in both places:

- installed copy under `$CODEX_HOME/skills/excel-date-understanding`
- workspace copy under `skills/excel-date-understanding`

the workspace copy should be treated as the portable package to keep in sync for future reuse and transfer.

## User Understanding Requirement

The skill should not optimize in a vacuum.

It should optimize in a way that matches:

- your workbook habits
- your explanation style
- your project-management logic
- your preferred judgment boundaries

If a proposed optimization conflicts with your existing guidance, it should be treated as pending until confirmed by you.

## Success Condition

The skill becomes stronger over time because:

- it keeps recognizing new reusable date-analysis techniques
- it proposes them explicitly
- you approve the useful ones
- every approved change is recorded

That makes the skill cumulative rather than static.
