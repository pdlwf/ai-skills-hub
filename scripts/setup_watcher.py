#!/usr/bin/env python3
"""
setup_watcher.py
Installs the ai-skills-hub watcher as a macOS launchd agent.
Run once: python3 scripts/setup_watcher.py
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent.resolve()
SOURCE_WATCHER = REPO_ROOT / "scripts" / "watcher.py"
DEPLOY_ROOT = Path.home() / ".ai-skills-hub"
WATCHER     = DEPLOY_ROOT / "watcher.py"
PLIST_NAME  = "com.pdlwf.ai-skills-hub.watcher"
PLIST_PATH  = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_NAME}.plist"
LOG_OUT     = DEPLOY_ROOT / "logs" / "watcher.stdout.log"
LOG_ERR     = DEPLOY_ROOT / "logs" / "watcher.stderr.log"

PLIST_CONTENT = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{PLIST_NAME}</string>

  <key>ProgramArguments</key>
  <array>
    <string>{sys.executable}</string>
    <string>{WATCHER}</string>
  </array>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>{LOG_OUT}</string>

  <key>StandardErrorPath</key>
  <string>{LOG_ERR}</string>

  <key>WorkingDirectory</key>
  <string>{DEPLOY_ROOT}</string>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    <key>AI_SKILLS_HUB_REPO_ROOT</key>
    <string>{REPO_ROOT}</string>
  </dict>
</dict>
</plist>
"""

def main():
    print("ai-skills-hub — Watcher Setup")
    print("─" * 40)

    # 1. Ensure logs dir
    DEPLOY_ROOT.mkdir(exist_ok=True)
    (DEPLOY_ROOT / "logs").mkdir(exist_ok=True)

    # 2. Deploy watcher to a local path outside cloud-synced storage.
    print(f"1. Deploying watcher → {WATCHER}")
    shutil.copy2(SOURCE_WATCHER, WATCHER)
    print("   ✓ watcher deployed")

    # 3. Install watchdog
    print("2. Installing watchdog...")
    subprocess.run([sys.executable, "-m", "pip", "install", "watchdog", "--quiet"], check=True)
    print("   ✓ watchdog installed")

    # 4. Write plist
    print(f"3. Writing launchd plist → {PLIST_PATH}")
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.write_text(PLIST_CONTENT)
    print("   ✓ plist written")

    # 5. Unload old if exists
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)],
                   capture_output=True)

    # 6. Load
    print("4. Loading launchd agent...")
    result = subprocess.run(["launchctl", "load", str(PLIST_PATH)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   ✗ Failed: {result.stderr}")
        sys.exit(1)
    print("   ✓ Agent loaded — will auto-start on login")

    # 7. Verify
    status = subprocess.run(["launchctl", "list", PLIST_NAME],
                             capture_output=True, text=True)
    if PLIST_NAME in status.stdout:
        print("\n✅ Watcher is running!")
    else:
        print("\n⚠ Agent loaded but may not be running yet. Check logs:")
        print(f"   tail -f {LOG_OUT}")

    print(f"\nUseful commands:")
    print(f"  Stop:    launchctl unload {PLIST_PATH}")
    print(f"  Start:   launchctl load {PLIST_PATH}")
    print(f"  Logs:    tail -f {LOG_OUT}")
    print(f"  Status:  launchctl list {PLIST_NAME}")

if __name__ == "__main__":
    main()
