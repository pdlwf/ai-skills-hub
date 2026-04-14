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

## Changelog

See [CHANGELOG.md](CHANGELOG.md)
