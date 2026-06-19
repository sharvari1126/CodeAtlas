from fastapi import FastAPI
from backend.scanner.repo_scanner import (
    clone_repository,
    analyze_repository
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse("frontend.html")

@app.post("/clone")
def clone_repo(repo_url: str):

    path = clone_repository(repo_url)

    return {
        "status": "success",
        "path": path
    }

@app.post("/analyze")
def analyze_repo(repo_url: str):

    try:

        repo_path = clone_repository(repo_url)

        results = analyze_repository(repo_path)

        return results

    except Exception as e:

        return {
            "error": str(e)
        }