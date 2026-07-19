import requests
from datetime import datetime
import time

# Constants
GITHUB_API_URL = "https://api.github.com/repos/relayhop/sn-monetization-runtime/issues"
TARGET_API_URL = "https://31day.cloud/api/bounties"
GITHUB_TOKEN = "your_github_token_here"
TARGET_API_KEY = "your_target_api_key_here"

# Headers for API requests
github_headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

target_headers = {
    "Authorization": f"Bearer {TARGET_API_KEY}",
    "Content-Type": "application/json"
}

def fetch_bounty_details(issue_number):
    url = f"{GITHUB_API_URL}/{issue_number}"
    response = requests.get(url, headers=github_headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def mirror_bounty(bounty_details):
    # Check if the bounty already exists on the target platform
    existing_bounty_url = f"{TARGET_API_URL}?source_issue={bounty_details['html_url']}"
    existing_response = requests.get(existing_bounty_url, headers=target_headers)
    if existing_response.status_code == 200 and existing_response.json():
        print(f"Bounty {bounty_details['html_url']} already exists on the target platform.")
        return

    # Prepare the data to be mirrored
    bounty_data = {
        "title": bounty_details["title"],
        "body": bounty_details["body"],
        "author": bounty_details["user"]["login"],
        "created_at": bounty_details["created_at"],
        "source_issue": bounty_details["html_url"],
        "labels": [label["name"] for label in bounty_details["labels"]],
        "comments": 0,
        "bounty_amount": None  # Assuming bounty amount is not specified in the issue
    }

    # Mirror the bounty to the target platform
    response = requests.post(TARGET_API_URL, json=bounty_data, headers=target_headers)
    if response.status_code == 201:
        print(f"Bounty {bounty_details['html_url']} successfully mirrored to the target platform.")
    else:
        response.raise_for_status()

def main():
    try:
        # Fetch the specific issue (bounty) details
        issue_number = 126
        bounty_details = fetch_bounty_details(issue_number)

        # Mirror the bounty details to the target platform
        mirror_bounty(bounty_details)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        # Handle rate limiting by waiting for a while before retrying
        if e.response.status_code == 429:
            retry_after = int(e.response.headers.get('Retry-After', '60'))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            main()  # Retry the operation

if __name__ == "__main__":
    main()