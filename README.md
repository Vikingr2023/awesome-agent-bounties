# Git Changelog Generator

This is a simple bash script that automatically generates a structured `CHANGELOG.md` file from your project's git history. It fetches commits since the last git tag and categorizes them into "Added", "Fixed", "Changed", and "Removed" sections.

## Features

*   **Automatic Categorization**: Commits are categorized based on conventional commit prefixes (e.g., `feat:`, `fix:`) and keywords in the commit message.
*   **Version Tracking**: Fetches commits since the last git tag, creating an "Unreleased" section for the latest changes.
*   **Markdown Output**: Generates a clean, readable `CHANGELOG.md` in Markdown format.
*   **Breaking Change Detection**: Highlights `BREAKING CHANGE` mentions in commit messages.

## Setup and Usage

1.  **Clone the repository (or copy the script)**:
    