from pathlib import Path
import sys

current_dir = Path(sys.modules['__main__'].__file__).parent

def get_path_or_none(file_path: str, extension: str):
    path = file_path.split(".")
    full_path = current_dir
    for p in path[:-1]:
        full_path = full_path / p
    full_path.mkdir(parents=True, exist_ok=True)
    
    file = Path(full_path / f"{path[-1]}.{extension}")
    
    if file.exists():
        return file
    
    return None

def get_path(file_path: str, extension: str):
    path = file_path.split(".")
    full_path = current_dir
    for p in path[:-1]:
        full_path = full_path / p
    full_path.mkdir(parents=True, exist_ok=True)

    file = Path(full_path / f"{path[-1]}.{extension}")
    return file