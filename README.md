# Weekly GitHub Repository Summary Workflow

## Setup Instructions

1. **Install n8n**: Follow the installation instructions from the [n8n documentation](https://docs.n8n.io).
2. **Import the Workflow**:
   - Go to your n8n instance.
   - Click on "Import" and upload the `workflow.json` file.
3. **Configure Variables**:
   - Set the `GitHub Repo Config` node with your GitHub repository.
   - Set the `Email Config` node with the recipient's email address.
   - Optionally, configure the language in the `Claude Summary` node.
4. **Test the Workflow**:
   - Run the workflow manually to ensure it works as expected.
   - Check the email to verify the summary is delivered correctly.
5. **Set Up Cron Trigger**:
   - The workflow is set to trigger weekly on Fridays at 5 PM. Adjust the cron expression if needed.

## Additional Notes
- Ensure you have the necessary API keys and credentials for GitHub and Claude API.
- Include a screenshot of the successful execution in your PR.

## Resources
- n8n docs: https://docs.n8n.io
- Claude API docs: https://docs.anthropic.com