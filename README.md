# Weekly GitHub Activity Summary Workflow

## Description
This n8n workflow generates a weekly narrative summary of a GitHub repository's activity using the Claude API and delivers it via email.

## Setup Instructions

1. **Install n8n**:
   ```bash
   npm install -g n8n
   ```

2. **Start n8n**:
   ```bash
   n8n
   ```

3. **Import the Workflow**:
   - Go to the n8n UI.
   - Click on "Import" and select the `workflow.json` file.

4. **Configure Variables**:
   - Set the `githubRepo` variable to your GitHub repository (e.g., `Vikingr2023/awesome-agent-bounties`).
   - Set the `emailDestination` variable to the email address where you want to receive the summary.

5. **Test the Workflow**:
   - Trigger the workflow manually or wait for the scheduled cron job to run.
   - Check your email for the summary.

## Configuration
- **GitHub Repository**: The GitHub repository to fetch activity from.
- **Email Destination**: The email address to send the summary to.
- **Language**: The language of the summary (EN/FR).

## Example
![Example Screenshot](example.png)

## Notes
- Ensure you have the necessary API keys for GitHub and Claude.
- The workflow is set to run every Friday at 5 PM.
