import subprocess
import requests
import logging
import json
from config import Config
from urllib.parse import urljoin
from base64 import b64encode
from nacl import encoding, public

logging.basicConfig(level=logging.INFO)

class GitHubClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {Config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

    def encrypt_secret(self, public_key: str, secret_value: str) -> tuple[str, str]:
        """Encrypt a secret using the repository's public key."""
        public_key_bytes = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key_bytes)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")

    def add_secret(self, repo_name: str, secret_name: str, secret_value: str) -> None:
        """Add a secret to a GitHub repository."""
        owner = Config.GITHUB_ORG or requests.get("https://api.github.com/user", headers=self.headers).json()["login"]
        
        # Get the public key for the repository
        key_url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/secrets/public-key"
        key_response = requests.get(key_url, headers=self.headers)
        key_data = key_response.json()
        
        if key_response.status_code != 200:
            raise Exception(f"Failed to get public key: {key_data.get('message')}")
        
        # Encrypt the secret
        encrypted_value = self.encrypt_secret(key_data["key"], secret_value)
        
        # Add the secret to the repository
        secret_url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/secrets/{secret_name}"
        payload = {
            "encrypted_value": encrypted_value,
            "key_id": key_data["key_id"]
        }
        
        response = requests.put(secret_url, headers=self.headers, json=payload)
        if response.status_code not in (201, 204):
            raise Exception(f"Failed to add secret: {response.json().get('message')}")

def create_webhook(repo_name: str, owner: str) -> dict:
    """Create a webhook for the repository to receive workflow run events."""
    headers = {
        "Authorization": f"token {Config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    # Construct webhook configuration
    webhook_url = urljoin(Config.API_BASE_URL, "/github/webhook")
    webhook_config = {
        "url": webhook_url,
        "content_type": "json",
        "secret": Config.GITHUB_WEBHOOK_SECRET,
        "insecure_ssl": "0"
    }
    
    # Events we want to receive
    events = ["workflow_run"]
    
    payload = {
        "name": "web",
        "active": True,
        "events": events,
        "config": webhook_config
    }
    
    github_api_url = f"https://api.github.com/repos/{owner}/{repo_name}/hooks"
    
    try:
        response = requests.post(github_api_url, headers=headers, json=payload)
        response_json = response.json()
        
        if response.status_code not in (200, 201):
            error_message = (
                f"GitHub Webhook Creation Error:\n"
                f"Status Code: {response.status_code}\n"
                f"Response: {json.dumps(response_json, indent=2)}"
            )
            logging.error(error_message)
            raise Exception(f"GitHub webhook creation failed: {response_json.get('message', 'Unknown error')}")
        
        logging.info(f"Successfully created webhook for {owner}/{repo_name}")
        return response_json
    except requests.exceptions.RequestException as e:
        error_message = f"GitHub API request failed during webhook creation: {str(e)}"
        logging.error(error_message)
        raise Exception(error_message)

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
        
        # After successful repo creation, set up the webhook
        owner = response_json.get("owner", {}).get("login")
        if owner:
            create_webhook(sanitized_name, owner)
        else:
            logging.error("Could not determine repository owner for webhook creation")
        
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