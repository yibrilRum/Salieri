import os
from datetime import datetime

def get_base_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def project_dir() -> str:
    return os.path.join(get_base_dir(), "projects")

def get_log_dir() -> str:
    return os.path.join(get_project_dir(), "logs")

def ensure_project_dir() -> None:
    os.makedirs(get_project_dir(), exist_ok=True)
    os.makedirs(get_log_dir(), exist_ok=True)

def project_path(filename: str) -> str:
    ensure_project_dir()
    return os.path.join(get_project_dir(), filename)

def log_path() -> str:
    ensure_project_dir()
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(get_log_dir(), f"session_log_{today}.txt")