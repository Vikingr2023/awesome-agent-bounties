#!/usr/bin/env python3
"""
Generate a structured CHANGELOG.md from git history.

Usage:
    python generate_changelog.py
    ./generate_changelog.py

Outputs CHANGELOG.md in the current directory.

Features:
- Fetch commits since the last git tag
- Auto-categorize commits into Added, Fixed, Changed, Removed
- Format output as a markdown CHANGELOG.md
"""

import subprocess
import re
from datetime import datetime

# Categories and their matching keywords in commit messages
CATEGORIES = {
    "Added": ["add", "added", "feature", "new"],
    "Fixed": ["fix", "fixed", "bug", "bugfix", "patch"],
    "Changed": ["change", "changed", "update", "updated", "improve", "improved", "refactor"],
    "Removed": ["remove", "removed", "delete", "deleted", "drop"],
}

def run_git_command(args):
    """Run a git command and return its output as a string."""
    result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_latest_tag():
    """Get the latest git tag, or None if none exists."""
    try:
        tag = run_git_command(["describe", "--tags", "--abbrev=0"])
        return tag
    except subprocess.CalledProcessError:
        return None

def get_commits_since_tag(tag):
    """Get commits since the given tag. If tag is None, get all commits."""
    rev_range = f"{tag}..HEAD" if tag else "HEAD"
    log_format = "%H%n%s%n%b%n==END=="
    raw_log = run_git_command(["log", rev_range, f"--pretty=format:{log_format}"])
    commits = []
    for entry in raw_log.split("==END==\n"):
        if not entry.strip():
            continue
        lines = entry.strip().split("\n")
        commit_hash = lines[0]
        subject = lines[1] if len(lines) > 1 else ""
        body = "\n".join(lines[2:]) if len(lines) > 2 else ""
        commits.append({"hash": commit_hash, "subject": subject, "body": body})
    return commits

def categorize_commit(subject, body):
    """Categorize a commit message into one of the categories or None."""
    message = (subject + "\n" + body).lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in message:
                return category
    return None

def format_changelog(commits, tag):
    """Format the changelog markdown text."""
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    header = f"## [{tag or 'Initial commit'}] - {date_str}\n\n"
    sections = {cat: [] for cat in CATEGORIES.keys()}

    for c in commits:
        cat = categorize_commit(c["subject"], c["body"])
        if cat:
            # Use subject line as entry, strip any trailing punctuation
            entry = c["subject"].rstrip(".")
            sections[cat].append(f"- {entry}")

    # Remove empty categories
    sections = {k: v for k, v in sections.items() if v}

    if not sections:
        return f"{header}No notable changes.\n"

    changelog = header
    for cat in ["Added", "Fixed", "Changed", "Removed"]:
        if cat in sections:
            changelog += f"### {cat}\n"
            changelog += "\n".join(sections[cat]) + "\n\n"
    return changelog

def main():
    latest_tag = get_latest_tag()
    commits = get_commits_since_tag(latest_tag)
    if not commits:
        print("No commits found since last tag.")
        return

    changelog_text = format_changelog(commits, latest_tag)
    with open("CHANGELOG.md", "w", encoding="utf-8") as f:
        f.write("# Changelog\n\n")
        f.write(changelog_text)

    print("CHANGELOG.md generated successfully.")

if __name__ == "__main__":
    main()
