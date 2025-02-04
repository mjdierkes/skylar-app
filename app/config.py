import os

class Config:
    DEBUG = True
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    CODEMAGIC_API_TOKEN = os.getenv('CODEMAGIC_API_TOKEN')
    WORKSPACE_DIR = os.path.expanduser('~/workspace') 