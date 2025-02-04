import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    PROJECTS_ROOT = os.getenv("PROJECTS_ROOT")
    COMPANY_IDENTIFIER = os.getenv("COMPANY_IDENTIFIER")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_ORG = os.getenv("GITHUB_ORG")
    XCODEGEN_PATH = os.getenv("XCODEGEN_PATH", "xcodegen")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.PROJECTS_ROOT:
            missing.append("PROJECTS_ROOT")
        if not cls.COMPANY_IDENTIFIER:
            missing.append("COMPANY_IDENTIFIER")
        if not cls.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

Config.validate() 