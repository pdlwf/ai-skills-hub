# ai-skills-hub 🧠

Personal AI skills library — version-controlled, multi-tool installable.

## Structure

```
skills/          ← Source of truth (edit here)
  personal/      ← Only personal skills sync root
    create-plan/
    docx/
    pdf/
    playwright/
    pptx/
    self_customize/
      ai-knowledge-os/
      excel-date-understanding/
      frontend-slides/
      inventus-docs-list/
      inventus-slides/
      personalized-coding-framework/
    xlsx/
adapters/        ← Per-tool install path config
scripts/         ← installer, watcher, launchd setup
.github/         ← Auto-changelog on push
```

## Quick Install

```bash
# Install all skills to Claude Code
python3 scripts/installer.py --tool claude-code

# Install specific skills
python3 scripts/installer.py --tool claude-code --skills docx,pdf,pptx

# Install to multiple tools
python3 scripts/installer.py --tool claude-code,chatgpt,codex

# Link self-customized skills into Codex, Claude Code, and Claude Cowork
python3 scripts/sync_self_customize.py

# Build Claude App upload packages for every self-customized skill
bash scripts/package-claude-app.sh --self-customize

# List available tools and skills
python3 scripts/installer.py --list
```

## Auto-Sync Setup (one-time)

```bash
# Start the file watcher (auto-push on change + desktop notification)
python3 scripts/setup_watcher.py
```

This installs a launchd agent that:
- Watches all skill directories + installed tool directories
- Auto-commits and pushes changes to GitHub
- Sends macOS desktop notifications on sync

## Self-Customized Skill Flow

`skills/personal/self_customize/` is the only source of truth for heavily
customized skills.

Claude Code and Codex can use these skills directly through symlinks:

```bash
python3 scripts/sync_self_customize.py
```

Claude App / Claude.ai skills are account-level uploads. Generate uploadable
packages from the same source, then upload the `.skill` or `.zip` files from
`dist/` in `Customize > Skills`:

```bash
bash scripts/package-claude-app.sh --self-customize
```

Claude App currently has no confirmed local silent-install path in this repo.
Treat the files in `dist/` as release artifacts to upload manually in Claude's
`Customize > Skills` UI when you want to publish a new snapshot.

When feedback changes a skill:
- In Codex or Claude Code, edit the canonical folder under
  `skills/personal/self_customize/<skill>/`; the symlinked local skill updates
  immediately.
- In Claude App / Claude.ai, the uploaded skill is a read-only release
  snapshot. Maintain changes from Codex or Claude Code in the repo source,
  then regenerate the affected package:

```bash
python3 scripts/sync_self_customize.py --skills <skill-name>
bash scripts/package-claude-app.sh <skill-name>
```

## Adapters

Each tool's install config lives in `adapters/<tool>.yaml`:

```yaml
name: claude-code
install_path: ~/.claude/skills
file_types: [.md, .yaml, .json]
```

## Skill Format

Each skill folder should contain:
- `SKILL.md` — main skill instructions
- `meta.yaml` — metadata (name, version, description, tags)
- Any supporting `.json` config files

### Recording Third-Party Sources

If a skill was copied from GitHub or another repository, record the upstream in
that skill's `meta.yaml` so you can resync it later.

Example:

```yaml
name: playwright
version: "1.0.0"
description: "Automate a real browser from the terminal."
tags:
  - browser-automation
compatible_tools:
  - claude-code
  - codex
author: pdlwf
updated: "2026-04-14"
source:
  type: git
  url: https://github.com/example/skills-repo.git
  ref: main
  path: skills/playwright
  exclude:
    - README.md
  last_sync_commit: 0123456789abcdef
  last_sync_at: "2026-04-14T08:00:00+00:00"
```

Field meanings:
- `type`: `local` for your own skills, `git` for vendored third-party skills.
- `url`: upstream repository URL.
- `ref`: branch, tag, or commit to sync from.
- `path`: subdirectory inside the upstream repo that maps to this local skill.
- `exclude`: optional glob patterns that should not be copied from upstream.
- `last_sync_commit`: commit actually synced last time.
- `last_sync_at`: UTC timestamp of the last successful sync.

Use the source manager script:

```bash
# List all skills and whether they track an upstream source
python3 scripts/skill_sources.py list

# Preview syncing one third-party skill from its upstream source
python3 scripts/skill_sources.py sync playwright --dry-run

# Sync it for real
python3 scripts/skill_sources.py sync playwright

# Also remove local files that disappeared upstream
python3 scripts/skill_sources.py sync playwright --clean
```

Recommended workflow:
- Self-authored skills: omit `source` or set `source.type: local`.
- Heavily customized personal skills: keep them under
  `skills/personal/self_customize/` and link them into tools with
  `python3 scripts/sync_self_customize.py`.
- Third-party skills you do not customize heavily: keep them `source.type: git`
  and resync with `scripts/skill_sources.py sync <skill>`.
- Third-party skills you customize a lot: fork the upstream repo first, then
  point `source.url` to your fork so later updates remain traceable.

## Changelog

See [CHANGELOG.md](CHANGELOG.md)
