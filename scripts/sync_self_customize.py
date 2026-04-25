#!/usr/bin/env python3
"""
Link self-customized skills into local tool skill directories.

The canonical source is:
  skills/personal/self_customize/<skill-name>

Codex, Claude Code, and Claude Cowork should reference that source instead of
maintaining independent copied edits.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
CUSTOM_DIR = REPO_ROOT / "skills" / "personal" / "self_customize"
COWORK_ROOT = Path.home() / "Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/6646b417-5fba-46c1-9b00-ebaca8cf6a31/a2604f6d-a95d-4ed4-b93b-56f8dc42bbd2"

TARGETS = {
    "codex": Path.home() / ".codex" / "skills",
    "claude-code": Path.home() / ".claude" / "skills",
    "claude-cowork": COWORK_ROOT / "skills",
}


def custom_skills() -> list[Path]:
    if not CUSTOM_DIR.exists():
        return []
    return sorted(
        path
        for path in CUSTOM_DIR.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    )


def read_description(skill_dir: Path) -> str:
    meta_path = skill_dir / "meta.yaml"
    if meta_path.exists():
        with meta_path.open() as fh:
            meta = yaml.safe_load(fh) or {}
        if meta.get("description"):
            return str(meta["description"])

    text = (skill_dir / "SKILL.md").read_text(errors="ignore").splitlines()
    for line in text:
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"')
    return f"{skill_dir.name} skill"


def backup_path(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return path.with_name(f"{path.name}.backup-{stamp}")


def link_dir(source: Path, destination: Path, dry_run: bool) -> str:
    if destination.is_symlink():
        if destination.resolve() == source.resolve():
            return "already linked"
        if dry_run:
            return f"would relink {destination}"
        destination.unlink()
    elif destination.exists():
        if destination.resolve() == source.resolve():
            return "already linked"
        backup = backup_path(destination)
        if dry_run:
            return f"would move existing {destination} to {backup} and link"
        shutil.move(str(destination), str(backup))

    if dry_run:
        return f"would link {destination} -> {source}"

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.symlink_to(source, target_is_directory=True)
    return "linked"


def update_cowork_manifest(skill_dirs: list[Path], dry_run: bool) -> None:
    manifest_path = COWORK_ROOT / "manifest.json"
    if not manifest_path.exists():
        print(f"  ! Claude Cowork manifest not found: {manifest_path}")
        return

    with manifest_path.open() as fh:
        manifest = json.load(fh)

    by_name = {
        entry.get("name") or entry.get("skillId"): entry
        for entry in manifest.get("skills", [])
    }

    changed = False
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    for skill_dir in skill_dirs:
        name = skill_dir.name
        description = read_description(skill_dir)
        if name in by_name:
            entry = by_name[name]
            entry["description"] = description
            entry["enabled"] = True
            entry["updatedAt"] = now
            print(f"  manifest: updated {name}")
        else:
            entry = {
                "skillId": name,
                "name": name,
                "description": description,
                "creatorType": "user",
                "updatedAt": now,
                "enabled": True,
            }
            manifest.setdefault("skills", []).insert(0, entry)
            print(f"  manifest: added {name}")
        changed = True

    if changed:
        manifest["lastUpdated"] = int(datetime.now().timestamp() * 1000)
        if dry_run:
            print("  [dry-run] would write Claude Cowork manifest")
        else:
            with manifest_path.open("w") as fh:
                json.dump(manifest, fh, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync self_customize skills by symlink")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skills", help="Comma-separated skill names; default is all self_customize skills")
    args = parser.parse_args()

    skills = custom_skills()
    if args.skills:
        wanted = {item.strip() for item in args.skills.split(",") if item.strip()}
        skills = [path for path in skills if path.name in wanted]

    if not skills:
        print(f"No self_customize skills found in {CUSTOM_DIR}")
        return 1

    for skill_dir in skills:
        print(skill_dir.name)
        for target_name, target_root in TARGETS.items():
            result = link_dir(skill_dir, target_root / skill_dir.name, args.dry_run)
            print(f"  {target_name}: {result}")

    update_cowork_manifest(skills, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
