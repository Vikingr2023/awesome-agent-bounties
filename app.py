import requests
from thirtyoneday import GitHubBountyHunter

# Constants
BOUNTY_URL = "https://gofrantic.com/bounties/104"
FUNDING_RECEIPT = "https://gofrantic.com/r/6140f51b"

# Function to claim the bounty
def claim_bounty():
    # Initialize the GitHubBountyHunter
    hunter = GitHubBountyHunter()

    # Authenticate (if required)
    hunter.authenticate(api_key="your_api_key_here")

    # Claim the bounty
    response = hunter.claim_bounty(bounty_url=BOUNTY_URL)

    if response.status_code == 200:
        print("Bounty claimed successfully!")
    else:
        print(f"Failed to claim bounty: {response.text}")

# Main function
if __name__ == "__main__":
    claim_bounty()