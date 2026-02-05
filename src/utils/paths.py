from pathlib import Path
import os

def get_project_root() -> Path:
    """
    Returns the absolute path to the project root directory.
    Assumes this file is located at <root>/src/utils/paths.py
    """
    return Path(__file__).resolve().parent.parent.parent

def resolve_resource(relative_path: str) -> Path:
    """
    Resolves a path relative to the project root and returns an absolute Path object.
    """
    return get_project_root() / relative_path

def ensure_dir(path: Path):
    """
    Ensures a directory exists.
    """
    path.mkdir(parents=True, exist_ok=True)
