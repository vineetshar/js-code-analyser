import os
import shutil
from pygit2 import clone_repository, GitError
from fastapi import HTTPException

def clone_repo(repo_url: str, dest: str) -> None:
    try:
        os.makedirs(dest)  # Ensure the destination directory exists
        clone_repository(repo_url, dest)
    except GitError as e:
        raise HTTPException(status_code=400, detail=f"Error cloning repository: {e}")

def delete_repo(repo_path: str) -> None:
    try:
        shutil.rmtree(repo_path)
    except OSError as e:
        raise HTTPException(status_code=400, detail=f"Error deleting repository: {e}")

def get_js_files(repo_path):
    js_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.js'):
                js_files.append(os.path.join(root, file))
    return js_files
