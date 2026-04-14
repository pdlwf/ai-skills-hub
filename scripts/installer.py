#!/usr/bin/env python3
"""
ai-skills-hub installer
Usage:
  python3 scripts/installer.py --tool claude
  python3 scripts/installer.py --tool claude,chatgpt,codex
  python3 scripts/installer.py --tool claude --skills docx,pdf
  python3 scripts/installer.py --list
"""

import argparse
import os
import shutil
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional

# ── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).parent.parent.resolve()
SKILLS_DIR  = REPO_ROOT / "skills" / "personal"
ADAPTERS_DIR = REPO_ROOT / "adapters"
TOOL_ALIASES = {
    "claude": "claude-code",
}

# ── Helpers ──────────────────────────────────────────────────────────────────
def canonical_tool_name(tool_name: str) -> str:
    return TOOL_ALIASES.get(tool_name, tool_name)

def load_adapter(tool_name: str) -> dict:
    canonical_name = canonical_tool_name(tool_name)
    path = ADAPTERS_DIR / f"{canonical_name}.yaml"
    if not path.exists():
        print(f"  ✗ No adapter found for '{tool_name}' (looked in {path})")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)

def list_tools() -> list[str]:
    return [p.stem for p in ADAPTERS_DIR.glob("*.yaml")]

def list_skills() -> list[str]:
    return [p.name for p in SKILLS_DIR.iterdir() if p.is_dir()]

def expand_path(p: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(p)))

def notify(title: str, message: str):
    """macOS desktop notification."""
    os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')

# ── Core install logic ────────────────────────────────────────────────────────
def install_skill(skill_name: str, adapter: dict, dry_run: bool = False) -> bool:
    src = SKILLS_DIR / skill_name
    if not src.exists():
        print(f"  ✗ Skill '{skill_name}' not found in {SKILLS_DIR}")
        return False

    dest_base = expand_path(adapter["install_path"])
    allowed_types = set(adapter.get("file_types", [".md", ".yaml", ".json"]))

    if adapter.get("skill_subfolder", True):
        dest = dest_base / skill_name
    else:
        dest = dest_base

    if not dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    copied = []
    for src_file in src.rglob("*"):
        if src_file.is_file() and src_file.suffix in allowed_types:
            rel = src_file.relative_to(src)
            dst_file = dest / rel
            if not dry_run:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
            copied.append(str(rel))

    if copied:
        status = "[dry-run] would copy" if dry_run else "✓ installed"
        print(f"  {status}: {skill_name} → {dest}  ({len(copied)} files)")
        return True
    else:
        print(f"  ⚠ {skill_name}: no matching files (types: {allowed_types})")
        return False

def install(tools: list[str], skills: Optional[list[str]], dry_run: bool):
    all_skills = list_skills()
    target_skills = skills if skills else all_skills

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Installing {len(target_skills)} skill(s) to {len(tools)} tool(s)\n")

    results = {}
    for tool in tools:
        print(f"📦 {tool}")
        adapter = load_adapter(tool)
        ok = []
        for skill in target_skills:
            if install_skill(skill, adapter, dry_run=dry_run):
                ok.append(skill)
        results[tool] = ok
        print()

    # Summary
    print("─" * 50)
    print("Summary:")
    for tool, installed in results.items():
        print(f"  {tool}: {len(installed)}/{len(target_skills)} skills installed")

    if not dry_run:
        notify(
            "ai-skills-hub",
            f"Installed {sum(len(v) for v in results.values())} skill(s) across {len(tools)} tool(s)"
        )

# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Install AI skills to local tool directories"
    )
    parser.add_argument("--tool",   help="Comma-separated tool names, e.g. claude,chatgpt,codex")
    parser.add_argument("--skills", help="Comma-separated skill names (default: all)")
    parser.add_argument("--list",   action="store_true", help="List available tools and skills")
    parser.add_argument("--dry-run", action="store_true", help="Preview without copying files")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable tools:")
        for t in sorted(list_tools()):
            a = load_adapter(t)
            print(f"  {t:<30} → {a['install_path']}")
        print("\nAvailable skills:")
        for s in sorted(list_skills()):
            meta_path = SKILLS_DIR / s / "meta.yaml"
            desc = ""
            if meta_path.exists():
                with open(meta_path) as f:
                    m = yaml.safe_load(f)
                    desc = m.get("description", "")
            print(f"  {s:<35} {desc}")
        return

    if not args.tool:
        parser.print_help()
        sys.exit(1)

    tools  = [t.strip() for t in args.tool.split(",")]
    skills = [s.strip() for s in args.skills.split(",")] if args.skills else None

    install(tools, skills, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
