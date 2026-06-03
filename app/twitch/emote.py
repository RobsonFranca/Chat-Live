import io
import time
import requests
from PIL import Image, ImageTk

from app.cache.cache_manager import __get_path_or_none__, __get_path__
from app.cache.config import Config

# https://static-cdn.jtvnw.net/emoticons/v2/58765/default/dark/1.0
# https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_4ea6b9356c584185911caa28385b0eb9/default/dark/1.0

def __get_url_emote__(id):
    return f"https://static-cdn.jtvnw.net/emoticons/v2/{id}/default/dark/1.0"

class EmoteImage():
    EMOTE_SIZE = (24, 24)
    
    def __init__(self, id: str):
        self.__dir_emotes__ = "emotes"
        self.__get_info__(id)
        self.imagem_tkinter_label = None
        
    def __get_info__(self, id: str):
        self.id = id
        self.frames = []
        self.frames_index = 0
        self.labels = []
        self.delay = 100
        self.last_update = time.time()
    
    def __get_image__(self):
        file_path = __get_path_or_none__(self.__dir_emotes__, self.id)
        if file_path:
            img = Image.open(file_path)
            try:
                while True:
                    frame_tk = ImageTk.PhotoImage(img.copy().resize(self.EMOTE_SIZE, Image.Resampling.LANCZOS).convert("RGBA"))
                    self.frames.append(frame_tk)
                    img.seek(img.tell() + 1)
            except EOFError:
                pass
        else:
            response = requests.get(__get_url_emote__(self.id), timeout=5)
            content_type = response.headers.get('content-type')
            dados_imagem = io.BytesIO(response.content)
            img = Image.open(dados_imagem)
            self.delay = img.info.get('duration', 100)
            img_list = []
            if content_type == 'image/gif':
                try:
                    while True:
                        img_list.append(img.copy().resize(self.EMOTE_SIZE, Image.Resampling.LANCZOS).convert("RGBA"))
                        frame_tk = ImageTk.PhotoImage(img_list[-1])
                        self.frames.append(frame_tk)
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass
                if Config.get("emote.save_emotes", True):
                    img_list[0].save(__get_path__(self.__dir_emotes__, self.id), format="PNG",save_all=True,append_images=img_list[1:],loop=0,duration=self.delay)
            else:
                self.frames.append(ImageTk.PhotoImage(img.resize(self.EMOTE_SIZE, Image.Resampling.LANCZOS).convert("RGBA")))
                if Config.get("emote.save_emotes", True):
                    img.save(__get_path__(self.__dir_emotes__, self.id), format="PNG")
        self.delay = img.info.get('duration', 100)
        
    def animation(self):
        if len(self.frames) > 1:
            now = time.time() * 1000
            if now - self.last_update >= self.delay:
                self.last_update = now
                self.frames_index = (self.frames_index + 1) % len(self.frames)
                
                label_aux = []
                for label in self.labels:
                    try:
                        if label.winfo_exists():
                            label.configure(image=self.frames[self.frames_index])
                            label.image = self.frames[self.frames_index]
                            label_aux.append(label)
                    except Exception as e:
                        print(f"Erro ao atualizar frame do emote {self.id}: {e}")
                        
                self.labels = label_aux
    
    def get_current_frame(self):
        if(len(self.frames) == 0):
            self.__get_image__()
        return self.frames[self.frames_index]
    
    def add_label(self, label):
        if len(self.frames) > 1:
            self.labels.append(label)

class Emote():
    EMOTE_SIZE = (24, 24)
    
    def __init__(self, EmoteImage: EmoteImage, positons: str):
        self.image = EmoteImage
        self.__get_info__(positons)
        
    def __get_info__(self, positons: str):
        self.position_in_text = [list(map(int, s.split("-"))) for s in positons.split(",")]
      
    def get_current_frame(self):
        return self.image.get_current_frame()
    
    def add_label(self, label):
        self.image.add_label(label)