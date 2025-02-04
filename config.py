import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    PROJECTS_ROOT = os.getenv("PROJECTS_ROOT")
    COMPANY_IDENTIFIER = os.getenv("COMPANY_IDENTIFIER")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_ORG = os.getenv("GITHUB_ORG")
    GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8888")  # URL where this API is hosted
    XCODEGEN_PATH = os.getenv("XCODEGEN_PATH", "xcodegen")
    APPETIZE_API_TOKEN = os.getenv("APPETIZE_API_TOKEN")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.PROJECTS_ROOT:
            missing.append("PROJECTS_ROOT")
        if not cls.COMPANY_IDENTIFIER:
            missing.append("COMPANY_IDENTIFIER")
        if not cls.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if not cls.GITHUB_WEBHOOK_SECRET:
            missing.append("GITHUB_WEBHOOK_SECRET")
        if not cls.API_BASE_URL:
            missing.append("API_BASE_URL")
        if not cls.APPETIZE_API_TOKEN:
            missing.append("APPETIZE_API_TOKEN")
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

Config.validate() 