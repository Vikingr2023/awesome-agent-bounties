#!/bin/bash

# changelog.sh - Generate a structured CHANGELOG.md from git history

# Get the latest tag, or empty if none
latest_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$latest_tag" ]; then
  # No tags found, get all commits
  commits=$(git log --pretty=format:"%H %s")
else
  # Get commits since latest tag
  commits=$(git log ${latest_tag}..HEAD --pretty=format:"%H %s")
fi

if [ -z "$commits" ]; then
  echo "No new commits since last tag ($latest_tag)."
  exit 0
fi

# Prepare changelog sections
added=""
fixed=""
changed=""
removed=""

while IFS= read -r line; do
  # Extract commit message (skip hash)
  msg="${line#* }"
  # Lowercase message for matching
  lmsg=$(echo "$msg" | tr '[:upper:]' '[:lower:]')

  if echo "$lmsg" | grep -qE '\b(add|added|feature|implement|introduce|create)\b'; then
    added+="- $msg\n"
  elif echo "$lmsg" | grep -qE '\b(fix|fixed|bug|patch|resolve|correct)\b'; then
    fixed+="- $msg\n"
  elif echo "$lmsg" | grep -qE '\b(change|changed|update|upgrade|modify|refactor|improve)\b'; then
    changed+="- $msg\n"
  elif echo "$lmsg" | grep -qE '\b(remove|removed|delete|drop|clean)\b'; then
    removed+="- $msg\n"
  fi
done <<< "$commits"

# Compose changelog content
changelog=""

if [ -n "$added" ]; then
  changelog+="## Added\n$added\n"
fi
if [ -n "$fixed" ]; then
  changelog+="## Fixed\n$fixed\n"
fi
if [ -n "$changed" ]; then
  changelog+="## Changed\n$changed\n"
fi
if [ -n "$removed" ]; then
  changelog+="## Removed\n$removed\n"
fi

if [ -z "$changelog" ]; then
  echo "No categorized commits found since last tag ($latest_tag)."
  exit 0
fi

# Write to CHANGELOG.md
echo -e "# Changelog\n\n$changelog" > CHANGELOG.md

echo "CHANGELOG.md generated successfully."
