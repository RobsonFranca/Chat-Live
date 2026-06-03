from pathlib import Path
import sys

from app.utils.file import get_path, get_path_or_none

current_dir = Path(sys.modules['__main__'].__file__).parent
cache_dir = f"{current_dir}.cache"

def __get_path_or_none__(dir, file_name):
    if(dir != ""):
        return get_path_or_none(f"{cache_dir}.{dir}.{file_name}", "cache")
    return get_path_or_none(f"{cache_dir}.{file_name}", "cache")

def __get_path__(dir, file_name):
    if(dir != ""):
        return get_path(f"{cache_dir}.{dir}.{file_name}", "cache")
    return get_path(f"{cache_dir}.{file_name}", "cache")

if __name__ == "__main__":
    # print(__get_path_or_none__("emotes","teste"))
    pass