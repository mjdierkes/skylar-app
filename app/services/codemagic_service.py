import requests
from app.exceptions import CodemagicError

class CodemagicService:
    """Service for interacting with the Codemagic CI/CD platform."""
    
    def __init__(self, api_token):
        if not api_token:
            raise ValueError("Codemagic API token is required")
        self.api_token = api_token
        self.api_url = 'https://api.codemagic.io/apps'

    def setup_project(self, repository_url):
        """
        Sets up the project in Codemagic.
        
        Args:
            repository_url (str): The SSH URL of the GitHub repository
            
        Returns:
            dict: The Codemagic app configuration
            
        Raises:
            CodemagicError: If the project setup fails
            ValueError: If repository_url is None or empty
        """
        if not repository_url:
            raise ValueError("Repository URL is required")
            
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': self.api_token
        }
        data = {
            'repositoryUrl': repository_url
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise CodemagicError(f"Failed to set up project in Codemagic: {str(e)}") 