# Update Rules

## Precedence

Apply precedence in this order:
1. Explicit hard constraint from the user
2. Explicit preference with clear override language
3. Stable implicit pattern with high confidence
4. Legacy principle with stale evidence

## Confidence Updates

Start from each signal `confidence_seed`.
Adjust confidence per event:
- Repeat confirmation in similar context: `+0.10`
- Cross-project consistency: `+0.10`
- Strong explicit statement: `+0.15`
- Partial rejection: `-0.15`
- Direct rejection: `-0.30`
- Long inactivity across many turns: `-0.05`

Clamp to `0.0-1.0`.

## Promotion and Demotion

Promote to `hard_constraint` when:
- The user uses strict language (`must`, `never`, `always`) and confirms permanence.

Demote to `soft_bias` when:
- The user marks rule as situational.
- Evidence shows repeated context exceptions.

## Conflict Resolution Logic

When conflict is detected:
1. Check scope mismatch before declaring contradiction.
2. If both rules can coexist by scope, convert to conditional override.
3. If coexistence fails, ask at most 2 clarifying questions.
4. Record explicit resolution and keep traceability.

## Override Semantics

Interpret user phrases as:
- `for this project`: project-scoped override.
- `from now on`: global override.
- `just this time`: temporary exception, no promotion.
- `replace old rule`: supersede prior principle explicitly.

## Versioning Policy

Create new version when:
- A principle is added, removed, or materially changed.
- Any hard constraint changes.
- Any conflict transitions from pending to resolved.

Do not create versions for wording-only edits with unchanged meaning.

## Persistence Commit Rules

After each material update:
1. Append/modify records in `signals`, `principles`, `conflicts`, and `versions`.
2. Update `current_version` and `last_updated_at`.
3. Refresh `summary` with active hard constraints and top principles.
4. Write to `state/framework-state.yaml` atomically when possible.

If persistence is unavailable, surface a warning so the user knows cross-session continuity is at risk.
