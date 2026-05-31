import json

from app.cache.cache_manager import __get_path__, __get_path_or_none__

class Config:
    _S_CONFIG = None
            
    def get_config():
        file = __get_path_or_none__("","config")
        if file is not None:
            with open(file, "r") as f:
                json_data = f.read()
                Config._S_CONFIG = json.loads(json_data)
                return
        Config._S_CONFIG = {}
        
    def save_config():
        file = __get_path__("","config")
        with open(file, "w") as f:
            json.dump(Config._S_CONFIG, f)

    def get(key, default=None):
        if Config._S_CONFIG is None:
            Config.get_config()
        split_key = key.split(".")
        current_dict = Config._S_CONFIG
        for k in split_key:
            current_dict = current_dict.get(k)
            if current_dict is None:
                return default
        return current_dict

    def set(key, value):
        if Config._S_CONFIG is None:
            Config.get_config()
        split_key = key.split(".")
        current_dict = Config._S_CONFIG
        for k in split_key[:-1]:
            current_dict = current_dict.setdefault(k, {})
        current_dict[split_key[-1]] = value
        Config.save_config()
        
if __name__ == "__main__":
    Config.set("test", "value")
    print(Config.get("test"))