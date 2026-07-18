import os
import requests
import configparser
from github import Github

# Configuration setup
config = configparser.ConfigParser()
config.read('config.ini')

# Configurable repository and token
REPO_OWNER = config.get('github','repo_owner')
REPO_NAME = config.get('github','repo_name')
GITHUB_TOKEN = config.get('github', 'github_token')

def get_github_token():
    """Retrieve GitHub token from environment variable or configuration."""
    if 'GITHUB_TOKEN' in os.environ:
        return os.environ['GITHUB_TOKEN']
    return GITHUB_TOKEN

def review_pr(pr):
    """Perform a code review on a given pull request."""
    review_comments = []
    
    # Example review checks (these should be expanded based on actual code review criteria)
    files = pr.get_files()
    for file in files:
        if file.filename.endswith(('.py', '.js')):
            content = file.patch.split('\n')
            for i, line in enumerate(content):
                if "SELECT *" in line:
                    review_comments.append(f"File: {file.filename}, Line: {i+1} - Avoid using SELECT *, specify columns instead.")
                if "print(" in line:
                    review_comments.append(f"File: {file.filename}, Line: {i+1} - Consider using a logging framework instead of print().")
    
    return review_comments

def main():
    token = get_github_token()
    g = Github(token)
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    
    try:
        pulls = repo.get_pulls(state='open')
        for pr in pulls:
            print(f"Reviewing PR #{pr.number}: {pr.title}")
            comments = review_pr(pr)
            for comment in comments:
                print(comment)
                # Uncomment below line to actually post comments on PR
                # pr.create_review_comment(comment, file_path=comment.split()[1], line=int(comment.split()[3]))
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        # Implement retry logic or more sophisticated error handling as needed

if __name__ == "__main__":
    main()
