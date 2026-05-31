import time
import tkinter as tk
import customtkinter as ctk

from app.cache.config import Config
from app.cache.emote_factory import EmoteFactory
from app.cache.user_color_factory import UserColorFactory

class Message():
    FONT_SIZE = 12
    CHAT_COLOR = "#18181b"
    GAP_VALUE = 1
    
    def __init__(self, text_message):
        self.__get_info__(text_message)
    
    def __get_info__(self, text_message):
        dict_aux = {}
        text_aux = text_message
        # Extraindo os dados e organizando em um dict
        while len(text_aux) > 0:
            if(text_aux.startswith("user-typ")):
                x = text_aux
                rest = "";
            else:
                [x, rest] = text_aux.split(";", 1)
            [p,v] = x.split("=",1)
            dict_aux[p] = v
            text_aux = rest
        
        self.user_id = dict_aux["user-id"]
        self.display_name = dict_aux["display-name"]
        self.color = dict_aux["color"] or UserColorFactory.get_color(self.user_id)
        self.emotes = EmoteFactory.get_emotes(dict_aux["emotes"] if "emotes" in dict_aux else "")
        self.user_type = self.__get_user_type__(dict_aux["user-type"])
        self.message = self.__get_message__()
    
    def __get_user_type__(self, user_type):
        try:
            return user_type.replace(":", " ", 1).split(":", 1)[1]
        except:
            return ""
        
    def __get_message__(self):
        r = [];
        pos_emote = {}
        for emote in self.emotes:
            for pos in emote.position_in_text:
                pos_emote[pos[0]] = (emote, pos)
        pos_emote = dict(sorted(pos_emote.items(), key=lambda item: item[0]))
        
        message_aux = self.user_type
        offset = 0
        for _, (emote, pos) in pos_emote.items():
            r.append(("text",message_aux[:pos[0]-offset]))
            r.append(("emote",emote))
            message_aux = message_aux[(pos[1]+1)-offset:]
            offset = pos[0] + (pos[1]+1 - pos[0])
        if(len(message_aux) > 0):
            r.append(("text",message_aux))
        return r
    
    def __set_nickname__(self, current_line):
        current_width = 0
        nickname = tk.Label(current_line,text=self.display_name,font=("Segoe UI", self.FONT_SIZE, "bold"),fg=self.color if self.color != "#000000" else "#343434",bg=Message.CHAT_COLOR,anchor="w")
        nickname.pack(side="left")
        nickname.update_idletasks()
        current_width += nickname.winfo_reqwidth()
        two_dots = tk.Label(current_line, text=":",fg="white",font=("Segoe UI", self.FONT_SIZE),bg=Message.CHAT_COLOR,anchor="w")
        two_dots.pack(side="left")
        two_dots.update_idletasks()
        current_width += two_dots.winfo_reqwidth()
        return current_width
    
    def create_tk(self, root):
        container_to_style = tk.Frame(root, bg=Message.CHAT_COLOR)
        container_to_style.pack(fill="x", pady=Message.GAP_VALUE)
        
        container = tk.Frame(container_to_style, bg=Message.CHAT_COLOR)
        container.pack(fill="x", pady=5,padx=5)

        current_line = tk.Frame(container, bg=Message.CHAT_COLOR)
        current_line.pack(anchor="w", fill="x")

        max_width = root.winfo_width()-2 or 300
        current_width = 0

        current_width += self.__set_nickname__(current_line)

        for type_, value in self.message:
            if type_ == "text":
                words = value.split(" ")

                for w in words:
                    test = tk.Label(current_line, text=w,font=("Segoe UI", self.FONT_SIZE),bg=Message.CHAT_COLOR)
                    test.update_idletasks()

                    if current_width + test.winfo_reqwidth() > max_width:
                        current_line = tk.Frame(container, bg=Message.CHAT_COLOR)
                        current_line.pack(anchor="w", fill="x")
                        current_width = 0

                    label = tk.Label(current_line,text=w,font=("Segoe UI", self.FONT_SIZE),fg="white",bg=Message.CHAT_COLOR,anchor="w")
                    label.pack(side="left")
                    label.update_idletasks()
                    current_width += label.winfo_reqwidth()

            elif type_ == "emote":
                img = value.get_tk_image()

                test = tk.Label(current_line, image=img)
                test.update_idletasks()

                if current_width + test.winfo_reqwidth() > max_width:
                    current_line = tk.Frame(container, bg=Message.CHAT_COLOR)
                    current_line.pack(anchor="w", fill="x")
                    current_width = 0

                label = tk.Label(current_line,image=img,bg=Message.CHAT_COLOR)
                label.image = img
                label.pack(side="left")
                label.update_idletasks()
                current_width += label.winfo_reqwidth()

        container_to_style.after(Config.get("message.display_time", 10) * 1000, container_to_style.destroy)

        return container_to_style