from fastapi import FastAPI
from routes.new_project import router as new_project_router
from routes.github_webhooks import router as github_webhook_router

app = FastAPI(title="Swift Project Creator API")

app.include_router(new_project_router)
app.include_router(github_webhook_router, prefix="/github", tags=["github"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8888, reload=True) 