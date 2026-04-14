# Framework Schema

## Purpose

Define a compact, inspectable structure for the user programming governance framework.

## Core Objects

### Signal

Fields:
- `id`: unique id
- `source`: `explicit` or `implicit`
- `language`: `en`, `zh`, or mixed
- `text`: normalized statement or interaction summary
- `context`: task or project context
- `timestamp`: ISO-8601 datetime
- `strength`: `weak`, `medium`, `strong`
- `confidence_seed`: float `0.0-1.0`
- `tags`: list such as `abstraction`, `testing`, `verbosity`, `risk`

### Principle

Fields:
- `id`: unique id
- `statement`: abstract guidance sentence
- `kind`: `hard_constraint`, `soft_bias`, `heuristic`, `default_behavior`
- `scope`: `global`, `project`, `domain`, `response_format`
- `priority`: integer `1-5` (5 highest)
- `confidence`: float `0.0-1.0`
- `evidence_ids`: linked signal ids
- `status`: `active`, `superseded`, `deprecated`
- `notes`: optional rationale

### Conflict

Fields:
- `id`: unique id
- `principle_a`: principle id
- `principle_b`: principle id
- `type`: `direct`, `conditional`, `scope_mismatch`
- `detected_at`: ISO-8601 datetime
- `resolution`: `pending`, `clarified`, `merged`, `overridden`
- `resolution_note`: concise decision note

### Framework Version

Fields:
- `version`: monotonically increasing label (example `v12`)
- `created_at`: ISO-8601 datetime
- `change_summary`: added/revised/deprecated principles
- `principle_ids`: active principles included
- `open_conflicts`: unresolved conflict ids

### Framework State

Fields:
- `state_version`: schema version (example `1`)
- `current_version`: latest framework version id
- `signals`: list of Signal objects
- `principles`: list of Principle objects
- `conflicts`: list of Conflict objects
- `versions`: list of Framework Version objects
- `last_updated_at`: ISO-8601 datetime
- `summary`: short human-readable digest of active policy

## Persistence File

Store runtime state in:
- `state/framework-state.yaml`

Treat this as the durable source for cross-session continuity.
If the file does not exist, initialize with empty arrays and `current_version: v0`.

## Minimal Render for Runtime

For regular coding responses, render policy as:
1. Hard constraints
2. Top global principles
3. Active project/domain overrides
4. One-line policy impact
