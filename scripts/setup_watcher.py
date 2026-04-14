#!/usr/bin/env python3
"""
setup_watcher.py
Installs the ai-skills-hub watcher as a macOS launchd agent.
Run once: python3 scripts/setup_watcher.py
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent.resolve()
WATCHER     = REPO_ROOT / "scripts" / "watcher.py"
PLIST_NAME  = "com.pdlwf.ai-skills-hub.watcher"
PLIST_PATH  = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_NAME}.plist"
LOG_OUT     = REPO_ROOT / "logs" / "watcher.stdout.log"
LOG_ERR     = REPO_ROOT / "logs" / "watcher.stderr.log"

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
  <string>{REPO_ROOT}</string>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
  </dict>
</dict>
</plist>
"""

def main():
    print("ai-skills-hub — Watcher Setup")
    print("─" * 40)

    # 1. Ensure logs dir
    (REPO_ROOT / "logs").mkdir(exist_ok=True)

    # 2. Install watchdog
    print("1. Installing watchdog...")
    subprocess.run([sys.executable, "-m", "pip", "install", "watchdog", "--quiet"], check=True)
    print("   ✓ watchdog installed")

    # 3. Write plist
    print(f"2. Writing launchd plist → {PLIST_PATH}")
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.write_text(PLIST_CONTENT)
    print("   ✓ plist written")

    # 4. Unload old if exists
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)],
                   capture_output=True)

    # 5. Load
    print("3. Loading launchd agent...")
    result = subprocess.run(["launchctl", "load", str(PLIST_PATH)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   ✗ Failed: {result.stderr}")
        sys.exit(1)
    print("   ✓ Agent loaded — will auto-start on login")

    # 6. Verify
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
