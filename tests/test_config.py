import os
import tempfile
from unittest.mock import patch
from app.config import load_config

@patch('app.config.load_dotenv')
def test_load_config(mock_load_dotenv):
    # Store original env var if it exists
    original_env = os.environ.get("ENV_FILE_PATH")
    original_token = os.environ.get("GITHUB_TOKEN")
    
    try:
        # Set up test environment
        os.environ["ENV_FILE_PATH"] = "/mock/path/config.env"
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["BASE_PROJECT_DIR"] = "/tmp/test_projects"
        
        config = load_config()
        
        assert config["GITHUB_TOKEN"] == "test_token"
        assert config["BASE_PROJECT_DIR"] == "/tmp/test_projects"
        mock_load_dotenv.assert_called_once()
    finally:
        # Restore original environment
        if original_env:
            os.environ["ENV_FILE_PATH"] = original_env
        else:
            del os.environ["ENV_FILE_PATH"]
            
        if original_token:
            os.environ["GITHUB_TOKEN"] = original_token
        else:
            del os.environ["GITHUB_TOKEN"]