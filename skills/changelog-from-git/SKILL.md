---
name: changelog-from-git
description: Generate a structured CHANGELOG.md from git commit history, grouped by Conventional Commit type (feat, fix, docs, chore, etc.) and release tag. Use when the user asks to create, update, or regenerate a changelog from git log/tags.
---

# Changelog From Git

Generate a structured `CHANGELOG.md` from the repository's git history.

## When to use this skill

Use this skill when the user asks to:
- Create or update a `CHANGELOG.md` file
- Summarize recent commits into release notes
- Produce a changelog grouped by version tag or by commit type

## How it works

1. Run `scripts/generate_changelog.sh` from the repository root. It reads git
   tags (as release boundaries) and commit messages, and groups commits under
   each release by [Conventional Commits](https://www.conventionalcommits.org/)
   type prefix (`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`,
   `build`, `ci`, `style`, `revert`).
2. Commits that don't match a known type prefix are placed under an "Other"
   section.
3. The script writes/overwrites `CHANGELOG.md` in the repository root.

## Usage

```bash
bash skills/changelog-from-git/scripts/generate_changelog.sh [output-file]
```

- `output-file` (optional): path to write the changelog to. Defaults to
  `CHANGELOG.md` in the current working directory.

## Example output

```markdown
# Changelog

## v1.2.0

### Features
- feat: add dark mode toggle (a1b2c3d)

### Bug Fixes
- fix: correct off-by-one error in pagination (e4f5a6b)

## v1.1.0

### Other
- initial import (0000001)
```

## Notes

- If the repository has no tags, all commits are grouped under an
  "Unreleased" heading.
- The script only reads git history; it makes no commits or pushes on its
  own. Review the generated file before committing it.
