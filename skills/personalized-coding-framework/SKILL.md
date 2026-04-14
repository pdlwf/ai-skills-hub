---
name: personalized-coding-framework
description: Global coding governance layer that applies the user’s programming constitution to every coding task. Use for any coding project work (planning, architecture, implementation, refactor, debugging, testing, reviews, and technical writing) to infer or update principles from explicit intent plus interaction signals, resolve preference conflicts, and condition decisions with the current framework.
---

# Personalized Coding Framework

## Operating Goal

Build and maintain a living abstraction layer that governs coding decisions across projects.
Fuse explicit user statements with revealed preferences from interaction outcomes.

## Trigger Conditions

Activate this skill when any of the following occurs:
- Any coding-related task begins and user governance should be applied by default.
- The user states preferences, constraints, or principles.
- The user accepts, rejects, or refines a technical proposal.
- The user asks to update, remove, compare, or inspect preferences.
- A new project starts and top-level governance should be applied.

## Core Workflow

0. Load Persistent State
- Open `state/framework-state.yaml` in this skill folder at the start of each coding task.
- If the file is missing, initialize it from `references/framework-schema.md` defaults.

1. Ingest Signals
- Extract explicit preferences from phrases such as `I want`, `I prefer`, `do not`, `must`, `should`, and equivalents in Chinese (`我希望`, `我不想`, `必须`, `不要`).
- Capture implicit signals from outcomes such as accept/reject, revision depth, and user pushback direction.
- Record each signal into persistent state with context, timestamp, scope guess, and confidence seed.

2. Synthesize Abstractions
- Convert raw signals into principles, heuristics, guardrails, and defaults.
- Classify each abstraction as hard constraint, soft bias, or situational preference.
- Assign scope: `global`, `project`, `domain`, or `response-format`.
- Update confidence using recurrence and consistency.

3. Detect and Resolve Conflicts
- Detect direct contradictions and conditional shifts.
- Treat new explicit intent as highest-priority candidate, then validate against recent behavior.
- Ask up to 2 clarifying questions only when conflict affects current decisions.
- Preserve conflict history; do not silently delete older principles.

4. Apply Framework as Policy
- Condition coding outputs on current framework before proposing solutions.
- Choose default abstraction level, structure, and trade-off framing based on active principles.
- If a requested output violates a hard constraint, flag the mismatch and request override confirmation.

5. Maintain Versions
- Create a new framework version for material updates.
- Summarize deltas in one concise block: added, revised, deprecated, confidence changes.
- Support user edit commands such as `remove principle`, `set as hard constraint`, `reset to prior`.

6. Persist Updates
- Save all accepted signal/principle/conflict/version changes back to `state/framework-state.yaml`.
- Keep only one authoritative current-state file and update `current_version` on each material change.

## Decision Hierarchy

Resolve decisions in this order:
1. User hard constraints (latest confirmed)
2. Global principles
3. Project-specific principles
4. Domain-specific heuristics
5. Formatting preferences

When two items conflict at the same level, prefer:
1. More recent explicit intent
2. Higher-confidence pattern
3. Narrower scope for local decisions

## Clarification Protocol

Ask clarifying questions only when necessary for correctness.
Use compact prompts:
1. `Is this a permanent preference or project-specific?`
2. `Should this override your existing default?`

If the user asks for speed, proceed with stated assumptions and label them.

## Output Contract

When this skill runs, provide:
- Applied principles: 2-5 bullets relevant to current task.
- Policy impact: one sentence on how these principles changed the approach.
- Optional update note when framework changed: version id and concise delta.

Keep this compact unless the user asks for full inspection.

## Persistent State

Use this file as the single source of truth for long-term preferences:
- `state/framework-state.yaml`

Minimum read/write behavior:
- Read before decisions.
- Write after material updates.
- Never silently drop prior principles; mark as superseded or deprecated with traceability.
- If write fails, report that persistence failed and continue with in-memory state for this turn only.

## Reference Files

Load these files as needed:
- `references/framework-schema.md`: data model and field definitions.
- `references/update-rules.md`: precedence, confidence, and conflict update logic.
- `references/operation-playbook.md`: procedural patterns and response templates.

## Boundaries

Do not claim certainty for low-confidence inferences.
Do not treat one-off exploration as a permanent preference without confirmation.
Do not apply project-local rules globally unless explicitly promoted.
