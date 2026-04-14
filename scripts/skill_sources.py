#!/usr/bin/env python3
"""
Manage upstream source metadata for skills vendored into this repository.

Examples:
  python3 scripts/skill_sources.py list
  python3 scripts/skill_sources.py sync playwright --dry-run
  python3 scripts/skill_sources.py sync playwright --clean
"""

from __future__ import annotations

import argparse
import fnmatch
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills" / "personal"
DEFAULT_EXCLUDES = [".git", ".git/**", "meta.yaml"]


def skill_dir(skill_name: str) -> Path:
    return SKILLS_DIR / skill_name


def load_meta(skill_name: str) -> tuple[Path, dict]:
    meta_path = skill_dir(skill_name) / "meta.yaml"
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing meta.yaml for skill '{skill_name}': {meta_path}")
    with meta_path.open() as fh:
        meta = yaml.safe_load(fh) or {}
    return meta_path, meta


def save_meta(meta_path: Path, meta: dict) -> None:
    with meta_path.open("w") as fh:
        yaml.safe_dump(meta, fh, sort_keys=False, allow_unicode=True)


def list_skill_names() -> list[str]:
    if not SKILLS_DIR.exists():
        return []
    return sorted(path.name for path in SKILLS_DIR.iterdir() if path.is_dir())


def source_config(meta: dict) -> dict:
    return meta.get("source") or {"type": "local"}


def require_git_source(skill_name: str, source: dict) -> None:
    source_type = source.get("type", "local")
    if source_type != "git":
        raise ValueError(
            f"Skill '{skill_name}' source.type is '{source_type}', only 'git' can be synced."
        )
    for required in ("url", "path"):
        if not source.get(required):
            raise ValueError(f"Skill '{skill_name}' source.{required} is required for git sync.")


def matches_any(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def collect_source_files(source_root: Path, excludes: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in source_root.rglob("*"):
        if not item.is_file():
            continue
        rel = item.relative_to(source_root).as_posix()
        if matches_any(rel, excludes):
            continue
        files.append(item)
    return sorted(files)


def resolve_ref_argument(source: dict, cli_ref: str | None) -> str | None:
    if cli_ref:
        return cli_ref
    if source.get("ref"):
        return str(source["ref"])
    return None


def clone_source(url: str, ref: str | None, temp_dir: Path) -> Path:
    clone_dir = temp_dir / "upstream"
    subprocess.run(["git", "clone", "--quiet", url, str(clone_dir)], check=True)
    if ref:
        subprocess.run(["git", "-C", str(clone_dir), "checkout", "--quiet", ref], check=True)
    return clone_dir


def git_output(repo_dir: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_dir), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def sync_skill(skill_name: str, ref_override: str | None, clean: bool, dry_run: bool) -> None:
    meta_path, meta = load_meta(skill_name)
    source = source_config(meta)
    require_git_source(skill_name, source)

    ref = resolve_ref_argument(source, ref_override)
    excludes = DEFAULT_EXCLUDES + list(source.get("exclude", []))
    destination = skill_dir(skill_name)

    with tempfile.TemporaryDirectory(prefix=f"skill-source-{skill_name}-") as temp_root:
        temp_dir = Path(temp_root)
        clone_dir = clone_source(str(source["url"]), ref, temp_dir)
        upstream_root = clone_dir / source["path"]
        if not upstream_root.exists():
            raise FileNotFoundError(
                f"Skill '{skill_name}' source.path does not exist in upstream: {source['path']}"
            )

        upstream_files = collect_source_files(upstream_root, excludes)
        upstream_rel = {file.relative_to(upstream_root).as_posix() for file in upstream_files}

        if clean:
            existing_files = [
                item for item in destination.rglob("*")
                if item.is_file() and item.name != "meta.yaml"
            ]
            stale_files = [
                file for file in existing_files
                if file.relative_to(destination).as_posix() not in upstream_rel
            ]
        else:
            stale_files = []

        action = "Would sync" if dry_run else "Syncing"
        print(f"{action} '{skill_name}' from {source['url']}")
        print(f"  source path: {source['path']}")
        print(f"  ref: {ref or '(default branch)'}")
        print(f"  files: {len(upstream_files)}")
        if clean:
            print(f"  stale files to remove: {len(stale_files)}")

        if dry_run:
            return

        for stale in stale_files:
            stale.unlink()

        for src_file in upstream_files:
            rel = src_file.relative_to(upstream_root)
            dest_file = destination / rel
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest_file)

        source["type"] = "git"
        source["last_sync_commit"] = git_output(clone_dir, "rev-parse", "HEAD")
        source["last_sync_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        if ref:
            source["ref"] = ref
        meta["source"] = source
        meta["updated"] = datetime.now().date().isoformat()
        save_meta(meta_path, meta)

        print(f"Completed sync for '{skill_name}'.")


def print_list() -> None:
    for skill_name in list_skill_names():
        _, meta = load_meta(skill_name)
        source = source_config(meta)
        source_type = source.get("type", "local")
        if source_type == "git":
            ref = source.get("ref", "(default branch)")
            last_commit = source.get("last_sync_commit", "-")
            short_commit = last_commit[:12] if last_commit != "-" else "-"
            print(
                f"{skill_name:<35} git  {source.get('url', '-')}"
                f"  ref={ref}  path={source.get('path', '-')}"
                f"  last={short_commit}"
            )
        else:
            print(f"{skill_name:<35} {source_type}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Track and sync third-party skill sources."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List skills and their source metadata")

    sync_parser = subparsers.add_parser("sync", help="Sync one git-backed skill from upstream")
    sync_parser.add_argument("skill", help="Skill directory name under skills/personal")
    sync_parser.add_argument("--ref", help="Override source.ref for this sync")
    sync_parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete local files that no longer exist upstream (except meta.yaml)",
    )
    sync_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without copying files",
    )

    args = parser.parse_args()

    try:
        if args.command == "list":
            print_list()
        elif args.command == "sync":
            sync_skill(args.skill, args.ref, clean=args.clean, dry_run=args.dry_run)
        else:
            parser.error(f"Unknown command: {args.command}")
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
