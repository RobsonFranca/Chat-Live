import io

import requests

from app.cache.cache_manager import __get_path_or_none__, __get_path__
from PIL import Image, ImageFile, ImageTk

# https://static-cdn.jtvnw.net/emoticons/v2/58765/default/dark/1.0
# https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_4ea6b9356c584185911caa28385b0eb9/default/dark/1.0

def __get_url_emote__(id):
    return f"https://static-cdn.jtvnw.net/emoticons/v2/{id}/default/dark/1.0"

class Emote():
    def __init__(self, id: str, positons: str):
        self.__dir_emotes__ = "emotes"
        self.__get_info__(id, positons)
        self.imagem_tkinter = None
        
    def __get_info__(self, id: str, positons: str):
        self.id = id
        self.position_in_text = [list(map(int, s.split("-"))) for s in positons.split(",")]
        self.image = None
    
    def __get_image__(self) -> ImageFile:
        file_path = __get_path_or_none__(self.__dir_emotes__, self.id)
        if file_path:
            img = Image.open(file_path)
        else:
            response = requests.get(__get_url_emote__(self.id), timeout=5)
            dados_imagem = io.BytesIO(response.content)
            img = Image.open(dados_imagem)
            img.save(__get_path__(self.__dir_emotes__, self.id), format="PNG")
        
        img = img.resize((20, 20), Image.Resampling.LANCZOS)
        return img
    
    def get_tk_image(self):
        if self.image is None:
            self.image = self.__get_image__()
            
        if(not self.imagem_tkinter):
            self.imagem_tkinter = ImageTk.PhotoImage(self.image)
        return self.imagem_tkinter