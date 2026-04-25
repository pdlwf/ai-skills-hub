#!/usr/bin/env python3
"""
ai-skills-hub installer
Usage:
  python3 scripts/installer.py --tool claude-code
  python3 scripts/installer.py --tool claude-code,claude-cowork,codex
  python3 scripts/installer.py --tool claude-cowork --skills docx,pdf
  python3 scripts/installer.py --list
  python3 scripts/installer.py --status
"""

import argparse
import os
import shutil
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

REPO_ROOT    = Path(__file__).parent.parent.resolve()
SKILLS_DIR   = REPO_ROOT / "skills" / "personal"
ADAPTERS_DIR = REPO_ROOT / "adapters"

# ── Helpers ──────────────────────────────────────────────────────────────────
def load_adapter(tool_name: str) -> dict:
    path = ADAPTERS_DIR / f"{tool_name}.yaml"
    if not path.exists():
        print(f"  ✗ No adapter found for '{tool_name}' (looked in {path})")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)

def list_tools() -> list[str]:
    return [p.stem for p in ADAPTERS_DIR.glob("*.yaml")]

def iter_skill_dirs() -> list[Path]:
    if not SKILLS_DIR.exists():
        return []
    return sorted(
        path.parent
        for path in SKILLS_DIR.rglob("SKILL.md")
        if not any(part.startswith(".") for part in path.relative_to(SKILLS_DIR).parts)
    )

def list_skills() -> list[str]:
    return [path.name for path in iter_skill_dirs()]

def resolve_skill_dir(skill_name: str) -> Optional[Path]:
    direct = SKILLS_DIR / skill_name
    if (direct / "SKILL.md").exists():
        return direct

    relative = SKILLS_DIR / skill_name
    if (relative / "SKILL.md").exists():
        return relative

    matches = [
        path
        for path in iter_skill_dirs()
        if path.name == skill_name or path.relative_to(SKILLS_DIR).as_posix() == skill_name
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"  ✗ Skill name '{skill_name}' is ambiguous:")
        for match in matches:
            print(f"    - {match.relative_to(SKILLS_DIR).as_posix()}")
        return None
    return None

def expand_path(p: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(p)))

def notify(title: str, message: str):
    os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')

def load_skill_meta(skill_name: str) -> dict:
    skill_path = resolve_skill_dir(skill_name)
    if not skill_path:
        return {}
    meta_path = skill_path / "meta.yaml"
    if meta_path.exists():
        with open(meta_path) as f:
            return yaml.safe_load(f) or {}
    return {}

# ── Core install ─────────────────────────────────────────────────────────────
def install_skill(skill_name: str, adapter: dict, dry_run: bool = False) -> bool:
    src = resolve_skill_dir(skill_name)
    if not src:
        print(f"  ✗ Skill '{skill_name}' not found in {SKILLS_DIR}")
        return False

    install_name = src.name
    dest_base     = expand_path(adapter["install_path"])
    allowed_types = set(adapter.get("file_types", [".md", ".yaml", ".json"]))
    dest          = dest_base / install_name if adapter.get("skill_subfolder", True) else dest_base

    if not dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    copied = []
    for src_file in src.rglob("*"):
        if src_file.is_file() and src_file.suffix in allowed_types:
            rel      = src_file.relative_to(src)
            dst_file = dest / rel
            if not dry_run:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
            copied.append(str(rel))

    if copied:
        status = "[dry-run] would copy" if dry_run else "✓ installed"
        print(f"  {status}: {install_name} → {dest}  ({len(copied)} files)")
        return True
    else:
        print(f"  ⚠ {skill_name}: no matching files (types: {allowed_types})")
        return False

# ── Cowork manifest update ───────────────────────────────────────────────────
def update_cowork_manifest(adapter: dict, skills: list[str], dry_run: bool = False):
    manifest_path = expand_path(adapter.get("manifest_path", ""))
    if not manifest_path or not manifest_path.exists():
        print("  ⚠ manifest_path not found, skipping manifest update")
        return

    with open(manifest_path) as f:
        manifest = json.load(f)

    existing = {
        (s.get("name") or s.get("skillId")): s
        for s in manifest.get("skills", [])
    }
    added = []

    for skill_name in skills:
        meta = load_skill_meta(skill_name)
        if skill_name in existing:
            if not dry_run:
                existing[skill_name]["description"] = meta.get(
                    "description",
                    existing[skill_name].get("description", f"{skill_name} skill"),
                )
                existing[skill_name]["enabled"] = True
                existing[skill_name]["updatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            print(f"  ↺ manifest: '{skill_name}' already registered")
            continue
        entry = {
            "skillId":     skill_name,
            "name":        skill_name,
            "description": meta.get("description", f"{skill_name} skill"),
            "creatorType": "user",
            "updatedAt":   datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "enabled":     True
        }
        if not dry_run:
            manifest["skills"].insert(0, entry)
        added.append(skill_name)

    if added and not dry_run:
        manifest["lastUpdated"] = int(datetime.now().timestamp() * 1000)
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"  ✓ manifest updated: added {added}")
    elif added:
        print(f"  [dry-run] would add to manifest: {added}")
    

# ── Status check ─────────────────────────────────────────────────────────────
def show_status():
    import hashlib

    def file_hash(p: Path) -> str:
        if not p.exists(): return "missing"
        return hashlib.md5(p.read_bytes()).hexdigest()[:8]

    skills = list_skills()
    tools  = list_tools()
    print(f"\n{'Skill':<35}", end="")
    for t in tools:
        print(f"{t:<20}", end="")
    print()
    print("─" * (35 + 20 * len(tools)))

    for skill in sorted(skills):
        src_md5 = file_hash(SKILLS_DIR / skill / "SKILL.md")
        print(f"{skill:<35}", end="")
        for tool in tools:
            adapter  = load_adapter(tool)
            skill_path = resolve_skill_dir(skill)
            install_name = skill_path.name if skill_path else skill
            dest     = expand_path(adapter["install_path"]) / install_name / "SKILL.md"
            dst_md5  = file_hash(dest)
            if dst_md5 == "missing":
                print(f"{'✗ not installed':<20}", end="")
            elif dst_md5 == src_md5:
                print(f"{'✓ in sync':<20}", end="")
            else:
                print(f"{'⚠ out of date':<20}", end="")
        print()
    print()

# ── Install orchestrator ──────────────────────────────────────────────────────
def install(tools: list[str], skills: Optional[list[str]], dry_run: bool):
    all_skills    = list_skills()
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
        # Extra step for cowork: update manifest
        if adapter.get("manifest_path"):
            update_cowork_manifest(adapter, ok, dry_run=dry_run)
        results[tool] = ok
        print()

    print("─" * 50)
    print("Summary:")
    for tool, installed in results.items():
        print(f"  {tool}: {len(installed)}/{len(target_skills)} skills installed")

    if not dry_run:
        notify("ai-skills-hub", f"Installed {sum(len(v) for v in results.values())} skill(s) across {len(tools)} tool(s)")

# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Install AI skills to local tool directories")
    parser.add_argument("--tool",    help="Comma-separated tool names, e.g. claude-code,claude-cowork,codex")
    parser.add_argument("--skills",  help="Comma-separated skill names (default: all)")
    parser.add_argument("--list",    action="store_true", help="List available tools and skills")
    parser.add_argument("--status",  action="store_true", help="Show sync status across all tools")
    parser.add_argument("--dry-run", action="store_true", help="Preview without copying files")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable tools:")
        for t in sorted(list_tools()):
            a = load_adapter(t)
            print(f"  {t:<30} → {a['install_path']}")
        print("\nAvailable skills:")
        for s in sorted(list_skills()):
            meta = load_skill_meta(s)
            print(f"  {s:<35} {meta.get('description','')[:60]}")
        return

    if args.status:
        show_status()
        return

    if not args.tool:
        parser.print_help()
        sys.exit(1)

    tools  = [t.strip() for t in args.tool.split(",")]
    skills = [s.strip() for s in args.skills.split(",")] if args.skills else None
    install(tools, skills, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
