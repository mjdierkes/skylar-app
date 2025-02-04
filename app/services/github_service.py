import subprocess
import os
from github import Github
from app.exceptions import GitHubError

class GitHubService:
    """Service for interacting with GitHub."""
    
    def __init__(self, github_token):
        if not github_token:
            raise ValueError("GitHub token is required")
        self.github = Github(github_token)

    def create_and_push_repository(self, project_name, project_path):
        """
        Creates a GitHub repository and pushes the initial code.
        
        Args:
            project_name (str): The name of the repository
            project_path (str): The local path to the project
            
        Returns:
            github.Repository.Repository: The created repository
            
        Raises:
            GitHubError: If repository creation or push fails
            ValueError: If project_name or project_path is None or empty
        """
        if not project_name or not project_path:
            raise ValueError("Project name and path are required")
            
        try:
            # Initialize git repository
            self._init_git_repo(project_path)

            # Create GitHub repository using gh CLI
            subprocess.run(['gh', 'repo', 'create', project_name, '--private', '--source', project_path, '--push'], 
                         cwd=project_path, check=True)

            # Get the repository object
            user = self.github.get_user()
            repo = user.get_repo(project_name)
            
            return repo
            
        except Exception as e:
            raise GitHubError(f"Failed to create or push to repository: {str(e)}")

    def _init_git_repo(self, project_path):
        """Initializes a git repository and creates the initial commit."""
        try:
            subprocess.run(['git', 'init'], cwd=project_path, check=True)
            subprocess.run(['git', 'add', '.'], cwd=project_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=project_path, check=True)
        except subprocess.CalledProcessError as e:
            raise GitHubError(f"Failed to initialize git repository: {str(e)}")

    def _push_to_remote(self, project_path, remote_url):
        """Adds the remote repository and pushes the code."""
        try:
            # Add remote and push using token in the URL
            token = os.getenv('GITHUB_TOKEN')
            url_with_token = f'https://{token}@github.com/{self.github.get_user().login}/{os.path.basename(project_path)}.git'
            subprocess.run(['git', 'remote', 'add', 'origin', url_with_token], cwd=project_path, check=True)
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=project_path, check=True)
        except subprocess.CalledProcessError as e:
            raise GitHubError(f"Failed to push to remote repository: {str(e)}") 