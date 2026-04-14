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
REPO_ROOT = Path(__file__).parent.parent.resolve()

# Directories to watch (source + all installed tool dirs)
WATCH_DIRS = [
    REPO_ROOT / "skills",                                               # source
    Path.home() / ".claude" / "skills",                                 # claude code
    Path.home() / ".codex" / "skills",                                  # codex
    Path.home() / "Library/Application Support/ChatGPT/skills",         # chatgpt desktop
]

# File types that trigger a sync
TRIGGER_EXTENSIONS = {".md", ".yaml", ".json"}

# Debounce: don't push more than once every N seconds
DEBOUNCE_SECONDS = 5

LOG_PATH = REPO_ROOT / "logs" / "watcher.log"
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
    skills_dir = REPO_ROOT / "skills"

    for watch_dir in WATCH_DIRS:
        if watch_dir == skills_dir:
            continue  # this IS the source
        try:
            rel = changed_path.relative_to(watch_dir)
            # rel = <skill-name>/<file>
            dest = skills_dir / rel
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
