#!/bin/bash

# Check if the repository has any tags
if [ -z "$(git tag)" ]; then
  echo "No tags found. Generating changelog for all commits."
  LAST_TAG="initial"
else
  # Get the latest tag
  LAST_TAG=$(git describe --tags --abbrev=0)
fi

# Initialize the changelog file
echo "# Changelog" > CHANGELOG.md

# Add the latest version header
echo "## [Unreleased] - $(date +%Y-%m-%d)" >> CHANGELOG.md

# Categorize and add commits to the changelog
git log --pretty=format:'%s' --since="$LAST_TAG" | while read -r commit; do
  case $commit in
    *add*|*Add*|*ADD*|*feat*|*Feat*|*FEAT*)
      echo "- **Added**: $commit" >> CHANGELOG.md
      ;;
    *fix*|*Fix*|*FIX*|*bug*|*Bug*|*BUG*)
      echo "- **Fixed**: $commit" >> CHANGELOG.md
      ;;
    *change*|*Change*|*CHANGE*|*refactor*|*Refactor*|*REFACTOR*|*update*|*Update*|*UPDATE*)
      echo "- **Changed**: $commit" >> CHANGELOG.md
      ;;
    *remove*|*Remove*|*REMOVE*|*del*|*Del*|*DEL*|*delete*|*Delete*|*DELETE*)
      echo "- **Removed**: $commit" >> CHANGELOG.md
      ;;
   *)
      echo "- **Other**: $commit" >> CHANGELOG.md
      ;;
  esac
done

# Add the previous version header
echo "## [$LAST_TAG] - $(git show -s --format='%ci' $LAST_TAG)" >> CHANGELOG.md

# Add the previous version changes
git log --pretty=format:'- %s' "$LAST_TAG"~1.."$LAST_TAG" >> CHANGELOG.md

echo "Changelog generated successfully: CHANGELOG.md"
