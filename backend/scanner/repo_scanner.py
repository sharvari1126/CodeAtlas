from git import Repo
import os

def clone_repository(repo_url):
    
    repo_name = repo_url.split("/")[-1].replace(".git", "")

    clone_path = os.path.join("repositories", repo_name)

    if os.path.exists(clone_path):
        return clone_path

    Repo.clone_from(repo_url, clone_path)

    return clone_path


def scan_repository(repo_path):

    all_files = []
    python_files = []

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            file_path = os.path.join(root, file)

            all_files.append(file_path)

            if file.endswith(".py"):
                python_files.append(file_path)

    return {
        "total_files": len(all_files),
        "python_files": python_files
    }