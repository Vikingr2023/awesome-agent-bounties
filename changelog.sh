#!/bin/bash

# changelog.sh - Generates a structured CHANGELOG.md from git history.

# --- Configuration ---
CHANGELOG_FILE="CHANGELOG.md"
DEFAULT_VERSION="Unreleased" # Version name for changes since the last tag
DATE_FORMAT="%Y-%m-%d"

# --- Helper Functions ---

# Function to get the latest tag
get_latest_tag() {
    git describe --tags --abbrev=0 2>/dev/null
}

# Function to get the commit hash of the latest tag
get_latest_tag_commit_hash() {
    local latest_tag=$(get_latest_tag)
    if [ -n "$latest_tag" ]; then
        git rev-list -n 1 "$latest_tag" 2>/dev/null
    fi
}

# Function to categorize a commit message
categorize_commit() {
    local message="$1"
    local category="Changed" # Default category

    # Convert message to lowercase for case-insensitive matching
    local lower_message=$(echo "$message" | tr '[:upper:]' '[:lower:]')

    # Prioritize conventional commit prefixes
    if [[ "$lower_message" =~ ^feat(\([a-zA-Z0-9_-]+\))?: ]]; then
        category="Added"
    elif [[ "$lower_message" =~ ^fix(\([a-zA-Z0-9_-]+\))?: ]]; then
        category="Fixed"
    elif [[ "$lower_message" =~ ^refactor(\([a-zA-Z0-9_-]+\))?: ]] || \
         [[ "$lower_message" =~ ^perf(\([a-zA-Z0-9_-]+\))?: ]] || \
         [[ "$lower_message" =~ ^style(\([a-zA-Z0-9_-]+\))?: ]] || \
         [[ "$lower_message" =~ ^revert(\([a-zA-Z0-9_-]+\))?: ]]; then
        category="Changed"
    elif [[ "$lower_message" =~ ^remove(\([a-zA-Z0-9_-]+\))?: ]] || \
         [[ "$lower_message" =~ ^deprecate(\([a-zA-Z0-9_-]+\))?: ]]; then
        category="Removed"
    # Fallback to keyword matching if no conventional prefix
    elif [[ "$lower_message" =~ ^(add|initial|new): ]] || \
         [[ "$lower_message" =~ "add " ]] || [[ "$lower_message" =~ "adds " ]] || [[ "$lower_message" =~ "added " ]] || \
         [[ "$lower_message" =~ "new feature" ]] || [[ "$lower_message" =~ "implement " ]] || [[ "$lower_message" =~ "introduce " ]]; then
        category="Added"
    elif [[ "$lower_message" =~ ^(fix|bug|resolve|patch): ]] || \
         [[ "$lower_message" =~ "fix " ]] || [[ "$lower_message" =~ "fixes " ]] || [[ "$lower_message" =~ "fixed " ]] || \
         [[ "$lower_message" =~ "resolve " ]] || [[ "$lower_message" =~ "resolves " ]] || [[ "$lower_message" =~ "resolved " ]] || \
         [[ "$lower_message" =~ "bug " ]] || [[ "$lower_message" =~ "correct " ]]; then
        category="Fixed"
    elif [[ "$lower_message" =~ ^(remove|delete|deprecate): ]] || \
         [[ "$lower_message" =~ "remove " ]] || [[ "$lower_message" =~ "removes " ]] || [[ "$lower_message" =~ "removed " ]] || \
         [[ "$lower_message" =~ "delete " ]] || [[ "$lower_message" =~ "deletes " ]] || [[ "$lower_message" =~ "deleted " ]] || \
         [[ "$lower_message" =~ "deprecate " ]]; then
        category="Removed"
    fi

    echo "$category"
}

# --- Main Script Logic ---

echo "Generating CHANGELOG.md..."

# Get the latest tag
LATEST_TAG=$(get_latest_tag)
LATEST_TAG_HASH=$(get_latest_tag_commit_hash)

# Determine the commit range
if [ -n "$LATEST_TAG" ]; then
    echo "Found latest tag: $LATEST_TAG. Fetching commits since then."
    COMMIT_RANGE="$LATEST_TAG..HEAD"
    CURRENT_VERSION_HEADER="$DEFAULT_VERSION"
else
    echo "No tags found. Fetching all commits."
    COMMIT_RANGE="HEAD"
    CURRENT_VERSION_HEADER="$DEFAULT_VERSION" # Or could be "Initial Release"
fi

# Get all commits in the range, including full body for breaking changes
# Format: %H (hash) | %s (subject) | %an (author name) | %b (body)
COMMITS=$(git log --pretty=format:"%H|%s|%an|%b" "$COMMIT_RANGE")

# Initialize associative arrays for categories
declare -A added_commits
declare -A fixed_commits
declare -A changed_commits
declare -A removed_commits

# Process commits
while IFS= read -r line; do
    COMMIT_HASH=$(echo "$line" | cut -d'|' -f1)
    COMMIT_SUBJECT=$(echo "$line" | cut -d'|' -f2)
    COMMIT_AUTHOR=$(echo "$line" | cut -d'|' -f3)
    COMMIT_BODY=$(echo "$line" | cut -d'|' -f4-) # Get the rest as body

    # Check for BREAKING CHANGE in subject or body
    local is_breaking_change=false
    if [[ "$COMMIT_SUBJECT" =~ "BREAKING CHANGE" ]] || [[ "$COMMIT_BODY" =~ "BREAKING CHANGE" ]]; then
        is_breaking_change=true
    fi

    # Categorize the commit
    CATEGORY=$(categorize_commit "$COMMIT_SUBJECT")

    # Clean up subject for display
    DISPLAY_SUBJECT=$(echo "$COMMIT_SUBJECT" | sed -E 's/^(feat|fix|build|chore|ci|docs|perf|refactor|revert|style|test|remove|deprecate|add|new|initial|bug|resolve|patch):[[:space:]]*//i')
    # Capitalize first letter of display subject
    DISPLAY_SUBJECT=$(echo "${DISPLAY_SUBJECT^}")

    # Add commit to appropriate category
    COMMIT_ENTRY="- $DISPLAY_SUBJECT ([`$COMMIT_HASH`](https://github.com/$(basename "$(pwd)")/commit/$COMMIT_HASH))"
    if [ "$is_breaking_change" = true ]; then
        COMMIT_ENTRY="- **BREAKING CHANGE**: $DISPLAY_SUBJECT ([`$COMMIT_HASH`](https://github.com/$(basename "$(pwd)")/commit/$COMMIT_HASH))"
        # Breaking changes are always "Changed"
        CATEGORY="Changed"
    fi

    case "$CATEGORY" in
        "Added")
            added_commits["$COMMIT_HASH"]="$COMMIT_ENTRY"
            ;;
        "Fixed")
            fixed_commits["$COMMIT_HASH"]="$COMMIT_ENTRY"
            ;;
        "Changed")
            changed_commits["$COMMIT_HASH"]="$COMMIT_ENTRY"
            ;;
        "Removed")
            removed_commits["$COMMIT_HASH"]="$COMMIT_ENTRY"
            ;;
    esac
done <<< "$COMMITS"

# --- Generate CHANGELOG content ---
CHANGELOG_CONTENT=""

# Add header for the current version
CURRENT_DATE=$(date +"$DATE_FORMAT")
CHANGELOG_CONTENT+="## $CURRENT_VERSION_HEADER ($CURRENT_DATE)\n\n"

# Add categorized changes
if [ ${#added_commits[@]} -gt 0 ]; then
    CHANGELOG_CONTENT+="### Added\n"
    for hash in "${!added_commits[@]}"; do
        CHANGELOG_CONTENT+="${added_commits[$hash]}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

if [ ${#fixed_commits[@]} -gt 0 ]; then
    CHANGELOG_CONTENT+="### Fixed\n"
    for hash in "${!fixed_commits[@]}"; do
        CHANGELOG_CONTENT+="${fixed_commits[$hash]}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

if [ ${#changed_commits[@]} -gt 0 ]; then
    CHANGELOG_CONTENT+="### Changed\n"
    for hash in "${!changed_commits[@]}"; do
        CHANGELOG_CONTENT+="${changed_commits[$hash]}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

if [ ${#removed_commits[@]} -gt 0 ]; then
    CHANGELOG_CONTENT+="### Removed\n"
    for hash in "${!removed_commits[@]}"; do
        CHANGELOG_CONTENT+="${removed_commits[$hash]}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# If no changes, add a note
if [ ${#added_commits[@]} -eq 0 ] && \
   [ ${#fixed_commits[@]} -eq 0 ] && \
   [ ${#changed_commits[@]} -eq 0 ] && \
   [ ${#removed_commits[@]} -eq 0 ]; then
    CHANGELOG_CONTENT+="*No significant changes.*\n\n"
fi

# Prepend the new content to the existing CHANGELOG.md if it exists
if [ -f "$CHANGELOG_FILE" ]; then
    echo "Prepending to existing $CHANGELOG_FILE..."
    # Remove the first line (main header) if it exists, to re-add it cleanly
    EXISTING_CONTENT=$(cat "$CHANGELOG_FILE" | sed '1d')
    echo "# Changelog\n\n${CHANGELOG_CONTENT}${EXISTING_CONTENT}" > "$CHANGELOG_FILE"
else
    echo "Creating new $CHANGELOG_FILE..."
    echo "# Changelog\n\n${CHANGELOG_CONTENT}" > "$CHANGELOG_FILE"
fi

echo "CHANGELOG.md generated successfully!"
echo "--- Sample Output ---"
head -n 20 "$CHANGELOG_FILE"
echo "---------------------"
