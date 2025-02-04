import subprocess
import requests
import logging
import json
from config import Config

logging.basicConfig(level=logging.INFO)

def create_github_repo(sanitized_name: str) -> dict:
    headers = {
        "Authorization": f"token {Config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    # Always create in user account for now
    github_api_url = "https://api.github.com/user/repos"
    logging.info("Creating repository in user account")

    payload = {
        "name": sanitized_name,
        "private": False,
        "auto_init": False,
        "description": f"SwiftUI project generated for {sanitized_name}"
    }

    logging.info(f"Making GitHub API request to: {github_api_url}")
    logging.info(f"Request payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(github_api_url, headers=headers, json=payload)
        response_json = response.json()
        
        logging.info(f"GitHub API response status: {response.status_code}")
        logging.info(f"GitHub API response headers: {dict(response.headers)}")
        logging.info(f"GitHub API response body: {json.dumps(response_json, indent=2)}")
        
        if response.status_code not in (200, 201):
            error_message = (
                f"GitHub API Error:\n"
                f"Status Code: {response.status_code}\n"
                f"Response: {json.dumps(response_json, indent=2)}\n"
                f"URL: {github_api_url}\n"
                f"Headers: {json.dumps({k: v for k, v in headers.items() if k != 'Authorization'}, indent=2)}"
            )
            logging.error(error_message)
            raise Exception(f"GitHub repo creation failed: {response_json.get('message', 'Unknown error')}")
        
        logging.info(f"Successfully created repository: {response_json.get('html_url')}")
        return response_json
    except requests.exceptions.RequestException as e:
        error_message = f"GitHub API request failed: {str(e)}"
        logging.error(error_message)
        raise Exception(error_message)

def push_to_github(project_dir: str, gh_repo: dict):
    clone_url = gh_repo.get("clone_url")
    if not clone_url:
        raise Exception("GitHub response missing clone URL.")

    logging.info(f"Pushing to GitHub repository: {clone_url}")

    try:
        # Configure git with token for HTTPS authentication
        git_url = clone_url.replace("https://", f"https://{Config.GITHUB_TOKEN}@")
        
        # Configure git user for this repository
        subprocess.run(["git", "config", "user.name", "Mason Dierkes"], cwd=project_dir, check=True)
        subprocess.run(["git", "config", "user.email", "mason@seedinnovate.com"], cwd=project_dir, check=True)
        
        logging.info("Git configuration complete")
        
        subprocess.run(["git", "remote", "remove", "origin"], cwd=project_dir, check=False)
        subprocess.run(["git", "remote", "add", "origin", git_url],
                       cwd=project_dir, check=True)
        logging.info("Git remote configured")
        
        subprocess.run(["git", "branch", "-M", "main"],
                       cwd=project_dir, check=True)
        logging.info("Git branch renamed to main")
        
        subprocess.run(["git", "push", "-u", "origin", "main"],
                       cwd=project_dir, check=True)
        logging.info(f"Successfully pushed to GitHub: {gh_repo.get('html_url')}")
    except subprocess.CalledProcessError as e:
        error_message = f"Git push failed: {str(e)}"
        logging.error(error_message)
        raise RuntimeError(error_message) 