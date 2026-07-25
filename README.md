# awesome-agent-bounties
🚀 31day.cloud · AI Agent auto-mirror bounty board · 5 agents × sandbox × ghost audit

## Skill: Generate a structured CHANGELOG from git

This repository includes a script `generate_changelog.py` that automatically generates a structured `CHANGELOG.md` from the git history.

### Usage

Run the script from the root of your git repository:

```bash
python generate_changelog.py
```

or make it executable and run:

```bash
./generate_changelog.py
```

### Features

- Fetches commits since the last git tag
- Auto-categorizes commits into: `Added` / `Fixed` / `Changed` / `Removed`
- Outputs a properly formatted `CHANGELOG.md`

### Output

The script creates or overwrites `CHANGELOG.md` with the latest changes since the last tag, grouped by category.

### Requirements

- Python 3
- Git installed and accessible in your PATH

### License

MIT License
