# ai-skills-hub 🧠

Personal AI skills library — version-controlled, multi-tool installable.

## Structure

```
skills/          ← Source of truth (edit here)
  create-plan/
  docx/
  excel-date-understanding/
  pdf/
  personalized-coding-framework/
  playwright/
  pptx/
  xlsx/
adapters/        ← Per-tool install path config
scripts/         ← installer, watcher, launchd setup
.github/         ← Auto-changelog on push
```

## Quick Install

```bash
# Install all skills to Claude Code
python3 scripts/installer.py --tool claude

# Install specific skills
python3 scripts/installer.py --tool claude --skills docx,pdf,pptx

# Install to multiple tools
python3 scripts/installer.py --tool claude,chatgpt,codex

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
- Third-party skills you do not customize heavily: keep them `source.type: git`
  and resync with `scripts/skill_sources.py sync <skill>`.
- Third-party skills you customize a lot: fork the upstream repo first, then
  point `source.url` to your fork so later updates remain traceable.

## Changelog

See [CHANGELOG.md](CHANGELOG.md)
