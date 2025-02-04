from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from services.swift_project import create_swift_project
from services.github_client import create_github_repo, push_to_github
from config import Config

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