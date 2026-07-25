name: generate-changelog
description: Generate a structured CHANGELOG.md from git history since last tag, categorized into Added, Fixed, Changed, Removed.
commands:
  - name: /generate-changelog
    description: Generate a structured CHANGELOG.md from git history since last tag
    run: bash changelog.sh
    output: CHANGELOG.md
    tests:
      - name: Check changelog file created
        run: test -f CHANGELOG.md
      - name: Check changelog contains date header
        run: grep -q "## " CHANGELOG.md
      - name: Check changelog contains at least one section
        run: grep -qE "### (Added|Fixed|Changed|Removed)" CHANGELOG.md
