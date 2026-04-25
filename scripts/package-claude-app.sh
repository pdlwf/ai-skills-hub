#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_ROOT="$REPO_ROOT/skills/personal"
DIST_DIR="$REPO_ROOT/dist"
TARGETS=()

fail() {
  echo "error: $*" >&2
  exit 1
}

find_skill_dir() {
  local name="$1"
  if [[ -d "$SKILLS_ROOT/$name" ]]; then
    printf '%s\n' "$SKILLS_ROOT/$name"
    return 0
  fi
  if [[ -d "$SKILLS_ROOT/self_customize/$name" ]]; then
    printf '%s\n' "$SKILLS_ROOT/self_customize/$name"
    return 0
  fi
  return 1
}

package_skill() {
  local name="$1"
  local skill_dir
  skill_dir="$(find_skill_dir "$name")" || fail "missing skill directory for: $name"
  local parent_dir
  parent_dir="$(dirname "$skill_dir")"
  local skill_base
  skill_base="$(basename "$skill_dir")"
  local skill_output="$DIST_DIR/$name.skill"
  local zip_output="$DIST_DIR/$name.zip"

  [[ -f "$skill_dir/SKILL.md" ]] || fail "missing SKILL.md: $skill_dir/SKILL.md"
  grep -q '^---$' "$skill_dir/SKILL.md" || fail "SKILL.md is missing YAML frontmatter delimiters"
  grep -q "^name: $name$" "$skill_dir/SKILL.md" || fail "SKILL.md frontmatter name does not match $name"
  grep -q '^description: ' "$skill_dir/SKILL.md" || fail "SKILL.md frontmatter is missing description"

  python3 - "$skill_dir/SKILL.md" <<'PY'
import sys
from pathlib import Path
import yaml

path = Path(sys.argv[1])
text = path.read_text(errors="ignore")
frontmatter = text.split("---", 2)[1]
data = yaml.safe_load(frontmatter) or {}
description = str(data.get("description", ""))
if len(description) > 200:
    raise SystemExit(f"{path}: description is {len(description)} chars; Claude.ai upload limit is 200")
PY

  rm -f "$skill_output" "$zip_output"

  (
    cd "$parent_dir"
    find "$skill_base" -name '.DS_Store' -delete
    zip -qr "$skill_output" "$skill_base" \
      -x "$skill_base/meta.yaml" \
      -x "$skill_base/agents/*" \
      -x "$skill_base/.git/*" \
      -x "$skill_base/__MACOSX/*"
  )

  cp "$skill_output" "$zip_output"
  echo "  $skill_output"
  echo "  $zip_output"
}

usage() {
  cat <<'EOF'
Usage:
  bash scripts/package-claude-app.sh <skill-name>
  bash scripts/package-claude-app.sh --self-customize

Notes:
  Claude App / Claude.ai skills are uploaded snapshots. This script only
  creates release artifacts in dist/; upload them manually in Customize > Skills.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --self-customize|--all-self-customize)
      TARGETS+=("__SELF_CUSTOMIZE__")
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      fail "unknown option: $1"
      ;;
    *)
      TARGETS+=("$1")
      shift
      ;;
  esac
done

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  TARGETS=("ai-knowledge-os")
fi

mkdir -p "$DIST_DIR"

echo "Claude App packages created:"
for target in "${TARGETS[@]}"; do
  if [[ "$target" == "__SELF_CUSTOMIZE__" ]]; then
    find "$SKILLS_ROOT/self_customize" -mindepth 1 -maxdepth 1 -type d | sort | while read -r dir; do
      package_skill "$(basename "$dir")"
    done
  else
    package_skill "$target"
    unzip -l "$DIST_DIR/$target.zip"
  fi
done
