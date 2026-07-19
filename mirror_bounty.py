import requests
import os
import git
from datetime import datetime

# Constants
SOURCE_REPO = "relayhop/sn-monetization-runtime"
SOURCE_ISSUE_NUMBER = 125
TARGET_REPO_PATH = "./target_repo"
README_PATH = "./target_repo/README.md"

# GitHub API URL for the specific issue
GITHUB_API_URL = f"https://api.github.com/repos/{SOURCE_REPO}/issues/{SOURCE_ISSUE_NUMBER}"

def fetch_bounty_info():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch issue: {response.status_code} - {response.text}")

def update_readme(bounty_info):
    with open(README_PATH, 'r') as file:
        readme_content = file.read()

    # Create a new section in the README.md
    readme_content += f"\n\n## Mirrored Bounty from {SOURCE_REPO}\n\n"
    readme_content += f"| 字段 | 值 |\n|---|---|\n"
    readme_content += f"| 源仓库 | {SOURCE_REPO} |\n"
    readme_content += f"| 原 issue | #{bounty_info['number']} |\n"
    readme_content += f"| 作者 | {bounty_info['user']['login']} |\n"
    readme_content += f"| 创建时间 | {bounty_info['created_at']} |\n"
    readme_content += f"| 标签 | {' '.join([label['name'] for label in bounty_info['labels']])} |\n"
    readme_content += f"| 评论 | {bounty_info['comments']} 条 |\n"
    readme_content += f"| 赏金 | 未注明 |\n"
    readme_content += f"| 原 URL | {bounty_info['html_url']} |\n\n"

    with open(README_PATH, 'w') as file:
        file.write(readme_content)

def mirror_bounty_to_repo(bounty_info):
    repo = git.Repo(TARGET_REPO_PATH)
    repo.git.add(README_PATH)
    repo.git.commit('-m', f"Add mirrored bounty from {SOURCE_REPO} issue #{bounty_info['number']}")
    repo.git.push('origin', 'main')

def main():
    try:
        # Fetch the bounty information
        bounty_info = fetch_bounty_info()

        # Update the README.md with the bounty information
        update_readme(bounty_info)

        # Mirror the bounty to the target repository
        mirror_bounty_to_repo(bounty_info)

        print("Bounty mirrored successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()