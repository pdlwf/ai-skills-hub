# Self-Customized Skills

This folder contains Bobby-authored or heavily customized skills. It is the canonical source for these skills across Codex, Claude Code, and Claude Cowork.

Rules:

- Edit skills here, not in installed tool folders.
- Link these skills into tool folders with `python3 scripts/sync_self_customize.py`.
- When feedback changes a skill's behavior, update the relevant folder here and rerun the sync script for that skill.
- Keep copied or upstream-vendored skills outside this folder unless Bobby has customized their behavior enough that this repo should own them.

Current self-customized skills:

- `ai-knowledge-os`
- `excel-date-understanding`
- `frontend-slides`
- `inventus-docs-list`
- `inventus-slides`
- `personalized-coding-framework`
