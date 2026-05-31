from pathlib import Path
import sys

current_dir = Path(sys.modules['__main__'].__file__).parent
cache_dir = current_dir / "cache"

def __get_path_or_none__(dir, file_name):
    if(dir != ""):
        dir_file = cache_dir / dir
        dir_file.mkdir(parents=True, exist_ok=True)
    else:
       dir_file = cache_dir 

    file = Path(dir_file / f"{file_name}.cache")
    if file.exists():
        return file
    
    return None

def __get_path__(dir, file_name):
    if(dir != ""):
        dir_file = cache_dir / dir
        dir_file.mkdir(parents=True, exist_ok=True)
    else:
       dir_file = cache_dir 

    file = Path(dir_file / f"{file_name}.cache")
   
    return file

if __name__ == "__main__":
    # print(__get_path_or_none__("emotes","teste"))
    pass