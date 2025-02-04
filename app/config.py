import os
from dotenv import load_dotenv
from pathlib import Path

# Default env file path; this can be swapped out at runtime.
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", "config.env")

def load_config(env_file: str = None):
    """
    Load configuration from an env file.
    If a new file is specified, it can hot-swap the settings.
    """
    env_file = env_file or ENV_FILE_PATH
    env_path = Path(env_file)
    if not env_path.exists():
        raise FileNotFoundError(f"Environment file {env_file} not found.")
    load_dotenv(dotenv_path=env_path, override=True)
    config = {
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "GITHUB_ORG": os.getenv("GITHUB_ORG", "default_org"),
        "APPETIZE_TOKEN": os.getenv("APPETIZE_TOKEN"),
        "APP_STORE_CONNECT_API_KEY": os.getenv("APP_STORE_CONNECT_API_KEY"),
        "BASE_PROJECT_DIR": os.getenv("BASE_PROJECT_DIR", "/tmp/xcode_projects"),
        "REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    }
    return config

# A global config variable that is reloaded each time build tasks are started.
config = load_config()