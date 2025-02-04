import os
import tempfile
from app.config import load_config

def test_load_config():
    # Create a temporary env file
    content = "GITHUB_TOKEN=test_token\nBASE_PROJECT_DIR=/tmp/test_projects\n"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    os.environ["ENV_FILE_PATH"] = tmp_path
    config = load_config()
    assert config["GITHUB_TOKEN"] == "test_token"
    assert config["BASE_PROJECT_DIR"] == "/tmp/test_projects"