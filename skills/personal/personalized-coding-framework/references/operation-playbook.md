# Operation Playbook

## Standard Cycle

1. Load `state/framework-state.yaml`.
2. Parse user turn for explicit preference language.
3. Parse reaction signals from acceptance, rejection, and refinements.
4. Map signals to one or more principles.
5. Recompute confidence and detect conflicts.
6. Apply current framework to current coding task.
7. Persist updates to `state/framework-state.yaml`.
8. Emit concise policy impact note when relevant.

## Signal Extraction Patterns

Explicit examples:
- `I prefer smaller steps first.`
- `Do not introduce another framework.`
- `I want short answers but complete decisions.`

Implicit examples:
- Repeatedly accepts incremental solutions.
- Rejects large up-front architecture proposals.
- Requests stronger challenge on weak assumptions.

## Response Templates

### Policy-Aware Proposal

Use:
1. `Applied principles`: 2-5 bullets
2. `Recommendation`: one preferred path
3. `Trade-offs`: concise and user-policy-aligned
4. `Optional alternative`: only when materially different

### Framework Update Notice

Use:
- `Framework update: v<new> from v<old>`
- `Added: ...`
- `Revised: ...`
- `Deprecated: ...`
- `Reason: ...`

### Clarification Prompt

Use only when needed:
1. `Is this a global preference or only for this project?`
2. `Should this replace your previous default?`

## Bilingual Handling

Treat English and Chinese preference statements as equal evidence.
Normalize multilingual statements into one canonical principle statement.
Keep original phrasing in evidence records for traceability.

## Anti-Patterns

Avoid:
- Inferring permanent rules from single-turn frustration.
- Dumping full framework when short policy snippet is enough.
- Ignoring explicit override language.
- Applying response-format preferences to architecture decisions.
- Skipping state writeback after a confirmed material preference update.
