from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from services.swift_project import create_swift_project
from services.github_client import create_github_repo, push_to_github
from config import Config
import subprocess
import logging
import os

router = APIRouter()

@router.post("/new")
async def new_project(request: Request):
    """
    Endpoint to create a new SwiftUI Xcode project.
    Expects a JSON payload:
      { "app_name": "My Awesome App" }
    """
    data = await request.json()
    if "app_name" not in data:
        raise HTTPException(status_code=400, detail="Missing app_name in request body")

    app_name = data["app_name"]
    response_data = {"message": "Project created successfully"}

    try:
        # Create the Swift project.
        project_dir, sanitized_name, bundle_identifier = create_swift_project(app_name)
        response_data["project_directory"] = project_dir
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating Swift project: {str(e)}")

    # Only attempt GitHub operations if token is available
    if Config.GITHUB_TOKEN and Config.GITHUB_TOKEN != "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN":
        try:
            # Create the GitHub repository.
            gh_repo = create_github_repo(sanitized_name)
            response_data["github_repo"] = gh_repo.get("html_url")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating GitHub repository: {str(e)}")

        try:
            # Push the initial commit to GitHub.
            push_to_github(project_dir, gh_repo)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error pushing to GitHub: {str(e)}")

    return JSONResponse(status_code=201, content=response_data)

@router.post("/commit")
async def commit_and_push(request: Request):
    """
    Endpoint to commit and push changes to GitHub.
    Expects a JSON payload:
      {
        "project_name": "MyProject",
        "commit_message": "Update project files"
      }
    """
    data = await request.json()
    if "project_name" not in data:
        raise HTTPException(status_code=400, detail="Missing project_name in request body")
    if "commit_message" not in data:
        raise HTTPException(status_code=400, detail="Missing commit_message in request body")

    project_name = data["project_name"]
    commit_message = data["commit_message"]
    project_dir = os.path.join(Config.PROJECTS_ROOT, project_name)

    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail=f"Project directory not found: {project_name}")

    response_data = {"message": "Changes committed and pushed successfully"}

    try:
        # Add all changes
        subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], cwd=project_dir, check=True)
        
        # Push changes
        subprocess.run(["git", "push", "origin", "main"], cwd=project_dir, check=True)
        
        logging.info(f"Successfully committed and pushed changes for {project_name}")
        return JSONResponse(status_code=200, content=response_data)
    except subprocess.CalledProcessError as e:
        error_message = f"Git operation failed: {str(e)}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message) 