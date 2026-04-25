#!/usr/bin/env python3
"""
ai-skills-hub watcher
Monitors skill source directories and all installed tool directories.
On change: auto git commit + push + macOS desktop notification.

Run via launchd (see scripts/setup_watcher.py), not directly.
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# ── watchdog ─────────────────────────────────────────────────────────────────
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Installing watchdog...")
    subprocess.run([sys.executable, "-m", "pip", "install", "watchdog", "--quiet"])
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

# ── Config ───────────────────────────────────────────────────────────────────
REPO_ROOT = Path(os.environ.get(
    "AI_SKILLS_HUB_REPO_ROOT",
    "/Users/bobby/Library/CloudStorage/OneDrive-个人/AI_study/skills_set/ai-skills-hub",
))

# Directories to watch (source + all installed tool dirs)
COWORK_SKILLS = Path.home() / "Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/6646b417-5fba-46c1-9b00-ebaca8cf6a31/a2604f6d-a95d-4ed4-b93b-56f8dc42bbd2/skills"

WATCH_DIRS = [
    REPO_ROOT / "skills" / "personal",                                  # source (repo)
    Path.home() / ".claude" / "skills",                                 # claude code
    Path.home() / ".codex" / "skills",                                  # codex
    COWORK_SKILLS,                                                       # claude app cowork
]

# File types that trigger a sync
TRIGGER_EXTENSIONS = {
    ".md", ".yaml", ".json",
    ".png", ".jpg", ".jpeg", ".svg",
    ".pptx", ".potx",
}

# Debounce: don't push more than once every N seconds
DEBOUNCE_SECONDS = 5

LOG_PATH = Path.home() / ".ai-skills-hub" / "logs" / "watcher.log"
LOG_PATH.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger("watcher")

# ── Notification ─────────────────────────────────────────────────────────────
def notify(title: str, message: str):
    os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')

# ── Git helpers ───────────────────────────────────────────────────────────────
def git_has_changes() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    return bool(result.stdout.strip())

def build_skills_context():
    """
    Generate SKILLS_CONTEXT.md — a single file summarising all personal skills.
    Used for pasting into Claude chat (conversation mode) as a quick context loader.
    """
    skills_dir = REPO_ROOT / "skills" / "personal"
    lines = [
        "# AI Skills Context",
        f"_Auto-generated {datetime.now().strftime('%Y-%m-%d %H:%M')} — paste into Claude chat to load all skills_\n",
    ]
    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        skill_path = skill_md.parent
        meta_yaml = skill_path / "meta.yaml"
        # Read description from meta.yaml
        desc = ""
        if meta_yaml.exists():
            for line in meta_yaml.read_text().splitlines():
                if line.startswith("description:"):
                    desc = line.replace("description:", "").strip().strip('"')
                    break
        lines.append(f"## {skill_path.name}")
        if desc:
            lines.append(f"_{desc}_\n")
        # Include first 30 lines of SKILL.md as preview
        skill_lines = skill_md.read_text().splitlines()[:30]
        lines.append("```")
        lines.extend(skill_lines)
        lines.append("```\n")

    out = REPO_ROOT / "SKILLS_CONTEXT.md"
    out.write_text("\n".join(lines))
    log.info(f"✓ SKILLS_CONTEXT.md updated ({len(list(skills_dir.rglob('SKILL.md')))} skills)")

def git_sync(changed_file: str):
    """Stage all, commit with timestamp, push."""
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        short = Path(changed_file).name

        subprocess.run(["git", "add", "-A"], cwd=REPO_ROOT, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"auto: update {short} [{ts}]"],
            cwd=REPO_ROOT, check=True
        )
        subprocess.run(["git", "push"], cwd=REPO_ROOT, check=True)

        # Rebuild context file for conversation mode
        build_skills_context()

        log.info(f"✓ Pushed: {changed_file}")
        notify("ai-skills-hub ✓", f"Synced: {short}")

    except subprocess.CalledProcessError as e:
        log.error(f"Git sync failed: {e}")
        notify("ai-skills-hub ✗", f"Sync failed — check logs")

# ── Watcher ───────────────────────────────────────────────────────────────────
class SkillHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_sync = 0.0

    def on_modified(self, event):
        self._handle(event)

    def on_created(self, event):
        self._handle(event)

    def on_deleted(self, event):
        self._handle(event)

    def _handle(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix not in TRIGGER_EXTENSIONS:
            return

        # Debounce
        now = time.time()
        if now - self._last_sync < DEBOUNCE_SECONDS:
            return
        self._last_sync = now

        log.info(f"Change detected: {event.src_path}")

        # If change is from an installed tool dir → copy back to source first
        _maybe_sync_back_to_source(path)

        if git_has_changes():
            git_sync(event.src_path)
        else:
            log.info("No git changes after file event (likely already in sync).")

def _maybe_sync_back_to_source(changed_path: Path):
    """
    If the change happened inside a tool install dir (not the repo),
    copy it back into skills/ so the repo stays as source of truth.
    """
    import shutil
    skills_dir = REPO_ROOT / "skills" / "personal"

    def source_skill_dir(skill_name: str) -> Path:
        custom = skills_dir / "self_customize" / skill_name
        if custom.exists():
            return custom
        return skills_dir / skill_name

    if not changed_path.exists():
        return

    for watch_dir in WATCH_DIRS:
        if watch_dir == skills_dir:
            continue  # this IS the source
        try:
            rel = changed_path.relative_to(watch_dir)
            # rel = <skill-name>/<file>
            if not rel.parts:
                continue
            dest = source_skill_dir(rel.parts[0]).joinpath(*rel.parts[1:])
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(changed_path, dest)
            log.info(f"  ↩ Synced back: {changed_path} → {dest}")
        except ValueError:
            continue  # not under this watch_dir

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    observer = Observer()
    handler  = SkillHandler()

    active = []
    for d in WATCH_DIRS:
        if d.exists():
            observer.schedule(handler, str(d), recursive=True)
            active.append(str(d))
            log.info(f"Watching: {d}")
        else:
            log.warning(f"Directory not found (skipped): {d}")

    if not active:
        log.error("No valid watch directories found. Exiting.")
        sys.exit(1)

    observer.start()
    log.info(f"Watcher started — monitoring {len(active)} director(ies)")
    notify("ai-skills-hub", f"Watcher started, monitoring {len(active)} directories")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log.info("Watcher stopped.")

    observer.join()

if __name__ == "__main__":
    main()
