import requests
import os
from app.exceptions import CodemagicError

class CodemagicService:
    """Service for interacting with the Codemagic CI/CD platform."""
    
    def __init__(self, api_token):
        if not api_token:
            raise ValueError("Codemagic API token is required")
        self.api_token = api_token
        self.api_url = 'https://api.codemagic.io'
        self.headers = {
            'Content-Type': 'application/json',
            'x-auth-token': self.api_token
        }

    def setup_project(self, repository_url):
        """
        Sets up the project in Codemagic.
        
        Args:
            repository_url (str): The HTTPS URL of the GitHub repository
            
        Returns:
            dict: The Codemagic app configuration with app ID
            
        Raises:
            CodemagicError: If the project setup fails
            ValueError: If repository_url is None or empty
        """
        if not repository_url:
            raise ValueError("Repository URL is required")
            
        # Add GitHub token to the repository URL for authentication
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token and 'https://' in repository_url:
            repository_url = repository_url.replace('https://', f'https://{github_token}@')
            
        data = {
            'repositoryUrl': repository_url
        }
        
        try:
            response = requests.post(f'{self.api_url}/apps', headers=self.headers, json=data)
            response.raise_for_status()
            app_data = response.json()
            
            # Start the first build
            app_id = app_data.get('_id')
            if app_id:
                self.start_build(app_id)
            
            return app_data
        except requests.exceptions.RequestException as e:
            raise CodemagicError(f"Failed to set up project in Codemagic: {str(e)}")

    def start_build(self, app_id, branch='main'):
        """
        Starts a new build for the specified app.
        
        Args:
            app_id (str): The Codemagic app ID
            branch (str, optional): The branch to build. Defaults to 'main'
            
        Raises:
            CodemagicError: If starting the build fails
            ValueError: If app_id is None or empty
        """
        if not app_id:
            raise ValueError("App ID is required")
            
        try:
            response = requests.post(
                f'{self.api_url}/builds',
                headers=self.headers,
                json={
                    'appId': app_id,
                    'workflowId': 'ios-workflow',  # Default workflow ID
                    'branch': branch
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise CodemagicError(f"Failed to start build: {str(e)}") 