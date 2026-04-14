#!/bin/bash
# bootstrap.sh
# Run once after SSH is configured.
# Creates the GitHub repo and pushes everything.
#
# Usage: bash scripts/bootstrap.sh

set -e

GITHUB_USER="pdlwf"
REPO_NAME="ai-skills-hub"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "╔══════════════════════════════════════╗"
echo "║   ai-skills-hub — Bootstrap Setup   ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── 1. Check SSH ─────────────────────────────────────────────────────────────
echo "1. Checking SSH connection to GitHub..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
  echo "   ✓ SSH OK"
else
  echo "   ✗ SSH not configured. Follow README Step 1 first."
  exit 1
fi

# ── 2. Check gh CLI or use curl ───────────────────────────────────────────────
echo ""
echo "2. Creating GitHub repository '$REPO_NAME'..."

if command -v gh &> /dev/null; then
  gh repo create "$REPO_NAME" --public --description "Personal AI skills library" || true
  echo "   ✓ Created via gh CLI"
else
  echo "   ℹ gh CLI not found — creating via API (needs GITHUB_TOKEN)"
  if [ -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo "   Either:"
    echo "   a) Install gh CLI:  brew install gh && gh auth login"
    echo "   b) Set token:       export GITHUB_TOKEN=your_token_here"
    echo "      Then re-run:     bash scripts/bootstrap.sh"
    exit 1
  fi
  curl -s -X POST https://api.github.com/user/repos \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$REPO_NAME\",\"public\":true,\"description\":\"Personal AI skills library\"}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print('   ✓ Created:', d.get('html_url','(check GitHub)'))"
fi

# ── 3. Copy skills from ~/.codex/skills ───────────────────────────────────────
echo ""
echo "3. Copying skills from ~/.codex/skills → $REPO_ROOT/skills ..."
SOURCE=~/.codex/skills
if [ -d "$SOURCE" ]; then
  cp -r "$SOURCE"/. "$REPO_ROOT/skills/"
  echo "   ✓ Skills copied"
else
  echo "   ⚠ ~/.codex/skills not found — skipping copy (add skills manually)"
fi

# ── 4. Git init + push ────────────────────────────────────────────────────────
echo ""
echo "4. Initialising git and pushing to GitHub..."
cd "$REPO_ROOT"

git init -b main
git remote remove origin 2>/dev/null || true
git remote add origin "git@github.com:$GITHUB_USER/$REPO_NAME.git"
git add -A
git commit -m "init: first commit — import skills and tooling"
git push -u origin main

echo ""
echo "✅ Done!"
echo ""
echo "Repo:      https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "Next steps:"
echo "  Install skills:  python3 scripts/installer.py --tool claude,chatgpt,codex"
echo "  Start watcher:   python3 scripts/setup_watcher.py"
