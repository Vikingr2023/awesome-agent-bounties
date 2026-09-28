#!/usr/bin/env bash
# Generate a structured CHANGELOG.md from git history, grouped by release tag
# and Conventional Commit type.
set -euo pipefail

OUTPUT_FILE="${1:-CHANGELOG.md}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository" >&2
  exit 1
fi

declare -A TYPE_LABELS=(
  [feat]="Features"
  [fix]="Bug Fixes"
  [docs]="Documentation"
  [refactor]="Refactoring"
  [perf]="Performance"
  [test]="Tests"
  [chore]="Chores"
  [build]="Build System"
  [ci]="Continuous Integration"
  [style]="Styling"
  [revert]="Reverts"
)
TYPE_ORDER=(feat fix perf refactor docs test build ci style chore revert)

# Print the commits in $1 (a git rev-range) grouped by Conventional Commit type.
emit_section() {
  local range="$1"
  local log
  log=$(git log --no-merges --pretty=format:'%h|%s' "$range" 2>/dev/null || true)
  [ -z "$log" ] && return 0

  declare -A grouped
  local other=""
  while IFS='|' read -r hash subject; do
    local type=""
    if [[ "$subject" =~ ^([a-zA-Z]+)(\([^\)]*\))?!?:\  ]]; then
      type=$(echo "${BASH_REMATCH[1]}" | tr '[:upper:]' '[:lower:]')
    fi
    if [[ -n "$type" && -n "${TYPE_LABELS[$type]:-}" ]]; then
      grouped[$type]+="- ${subject} (${hash})"$'\n'
    else
      other+="- ${subject} (${hash})"$'\n'
    fi
  done <<< "$log"

  for type in "${TYPE_ORDER[@]}"; do
    if [[ -n "${grouped[$type]:-}" ]]; then
      echo ""
      echo "### ${TYPE_LABELS[$type]}"
      printf '%s' "${grouped[$type]}"
    fi
  done
  if [[ -n "$other" ]]; then
    echo ""
    echo "### Other"
    printf '%s' "$other"
  fi
}

{
  echo "# Changelog"

  tags=$(git tag --sort=-creatordate 2>/dev/null || true)
  if [[ -z "$tags" ]]; then
    echo ""
    echo "## Unreleased"
    emit_section "HEAD"
  else
    prev=""
    for tag in $tags; do
      echo ""
      echo "## ${tag}"
      if [[ -n "$prev" ]]; then
        emit_section "${tag}..${prev}"
      else
        emit_section "${tag}"
      fi
      prev="$tag"
    done
  fi
} > "$OUTPUT_FILE"

echo "Changelog written to ${OUTPUT_FILE}" >&2
