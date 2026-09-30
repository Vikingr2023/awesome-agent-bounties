---
name: generate-changelog
description: Generate or update CHANGELOG.md from git history since the most recent tag.
---

# Generate CHANGELOG

Generate a structured CHANGELOG.md from this repository's real git history.

## Procedure
1. Run `git describe --tags --abbrev=0 2>/dev/null || true` to find the most recent tag.
2. If a tag exists, inspect `git log --no-merges <tag>..HEAD`; otherwise inspect all commits reachable from HEAD.
3. Read commit hash and subject with `git log --no-merges --pretty=format:'%h%x09%s'`.
4. Categorize every new commit into exactly one section: Added, Fixed, Changed, or Removed.
5. Prefer Conventional Commit prefixes when present: feat -> Added, fix -> Fixed, remove/delete -> Removed; everything else -> Changed.
6. Preserve existing released CHANGELOG sections. Update only the Unreleased section unless the user explicitly asks for a release.
7. Include each short commit hash in parentheses so every entry is traceable.
8. Never invent commits, dates, tags, issues, or changes. If there are no commits since the latest tag, report that and do not manufacture entries.

## Output shape
```markdown
# Changelog

## Unreleased

### Added
- Description (abc1234)

### Fixed
- Description (def5678)

### Changed
- Description (012abcd)

### Removed
- Description (345efgh)
```

Omit empty categories. Write the final result to CHANGELOG.md.
