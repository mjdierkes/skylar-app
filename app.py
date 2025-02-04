from fastapi import FastAPI
from routes.new_project import router as new_project_router

app = FastAPI(title="Swift Project Creator API")

app.include_router(new_project_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8888, reload=True) 