#!/bin/bash

# Ensure the script is run from the root of the repository
if [ ! -d .git ]; then
  echo "Error: This script must be run from the root of a git repository."
  exit 1
fi

# Fetch commit messages since the last git tag
commits=$(git log --pretty=format:'%s' $(git describe --tags --abbrev=0)..HEAD)

# Initialize variables for changelog sections
added=""
fixed=""
changed=""
removed=""

# Function to categorize commit messages
categorize_commit() {
  local message=$1
  if echo "$message" | grep -iqE "\b(add|added|adding|new|create|created|creating)\b"; then
    added+="* $message\n"
  elif echo "$message" | grep -iqE "\b(fix|fixed|fixing|bug|resolve|resolved|resolving)\b"; then
    fixed+="* $message\n"
  elif echo "$message" | grep -iqE "\b(change|changed|changing|update|updated|updating|modify|modified|modifying)\b"; then
    changed+="* $message\n"
  elif echo "$message" | grep -iqE "\b(remove|removed|removing|delete|deleted|deleting)\b"; then
    removed+="* $message\n"
  fi
}

# Categorize each commit message
while IFS= read -r commit; do
  categorize_commit "$commit"
done <<< "$commits"

# Generate CHANGELOG.md
changelog="## Changelog\n\n"

if [ -n "$added" ]; then
  changelog+="### Added\n\n$added\n"
fi

if [ -n "$fixed" ]; then
  changelog+="### Fixed\n\n$fixed\n"
fi

if [ -n "$changed" ]; then
  changelog+="### Changed\n\n$changed\n"
fi

if [ -n "$removed" ]; then
  changelog+="### Removed\n\n$removed\n"
fi

# Write to CHANGELOG.md
echo -e "$changelog" > CHANGELOG.md

echo "Changelog generated successfully."
