from fastapi import FastAPI
from backend.scanner.repo_scanner import (
    clone_repository,
    analyze_repository
)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to CodeAtlas"}

@app.post("/clone")
def clone_repo(repo_url: str):

    path = clone_repository(repo_url)

    return {
        "status": "success",
        "path": path
    }

@app.post("/analyze")
def analyze_repo(repo_url: str):

    repo_path = clone_repository(repo_url)

    results = analyze_repository(repo_path)

    return results