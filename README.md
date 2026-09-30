# awesome-agent-bounties
🚀 31day.cloud · AI Agent auto-mirror bounty board · 5 agents × sandbox × ghost audit
---

## Generate CHANGELOG with Claude Code

The repository includes a project-local `/generate-changelog` skill at `.claude/skills/generate-changelog/SKILL.md`.

Setup and use:
1. Open this repository in Claude Code.
2. Run `/generate-changelog`.
3. Review the generated `CHANGELOG.md` and commit it.

### Sample output from this repository

Using the repository history present when the skill was added:

```markdown
# Changelog

## Unreleased

### Added
- initial README with bounty board (1aeae2a)

### Changed
- Initial commit (a80a580)
```

The skill always reads the current git history; the sample above is evidence of the expected structure, not hard-coded generated output.
