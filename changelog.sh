#!/bin/bash

# changelog.sh - Generate a structured CHANGELOG.md from git history since last tag

set -e

# Get the last git tag
last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$last_tag" ]; then
  echo "No tags found, using initial commit as start point"
  start_point=$(git rev-list --max-parents=0 HEAD)
else
  start_point=$last_tag
fi

# Get commits since last tag or initial commit
commits=$(git log --pretty=format:"%s" "$start_point"..HEAD)

# Initialize changelog sections
added=""
fixed=""
changed=""
removed=""

# Categorize commits by prefix
while IFS= read -r line; do
  case "$line" in
    Added*|added*|Add*|add*)
      added+="$line"$'\n'
      ;;
    Fixed*|fixed*|Fix*|fix*)
      fixed+="$line"$'\n'
      ;;
    Changed*|changed*|Change*|change*)
      changed+="$line"$'\n'
      ;;
    Removed*|removed*|Remove*|remove*)
      removed+="$line"$'\n'
      ;;
    *)
      # Ignore other commits
      ;;
  esac
done <<< "$commits"

# Compose CHANGELOG.md content
{
  echo "# Changelog"
  echo
  echo "## $(date +%Y-%m-%d)"
  echo
  if [ -n "$added" ]; then
    echo "### Added"
    echo "$added"
  fi
  if [ -n "$fixed" ]; then
    echo "### Fixed"
    echo "$fixed"
  fi
  if [ -n "$changed" ]; then
    echo "### Changed"
    echo "$changed"
  fi
  if [ -n "$removed" ]; then
    echo "### Removed"
    echo "$removed"
  fi
} > CHANGELOG.md

echo "CHANGELOG.md generated successfully."
