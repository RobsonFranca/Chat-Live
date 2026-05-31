import os
import tkinter as tk
from tkinter import messagebox

import psutil

from app.cache.config import Config
from app.twitch.connection import ChannelNotFoundError, TwitchConnection
from app.ui.chat_window import ChatWindow
from app.twitch.message import Message

class ConfigWindow(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Chat Twitch")
        self.geometry("400x400")
        self.configure(bg="#333333")
        self.wm_attributes("-topmost", True)
        self.resizable(width=False, height=False)
        
        self.__construct_window__()
        
        self.connected = False
        self.chat.change_fixed(self.connected)
        
        self.__mem__()    
    
    def __mem__(self):
        proccess = psutil.Process(os.getpid())
        memo_bytes = proccess.memory_info().rss
        size_unit = "Bytes"
        
        if memo_bytes > 1024:
            memo_bytes /= 1024
            size_unit = "KB"
        if memo_bytes > 1024:
            memo_bytes /= 1024
            size_unit = "MB"
        if memo_bytes > 1024:
            memo_bytes /= 1024
            size_unit = "GB"

        self.label_memory.config(text=f"Memória: {memo_bytes:.2f} {size_unit}")

        self.after(5000, self.__mem__)
    
    def __construct_window__(self):
        self.title_wiindow = tk.Label(self, text="Configurações do Chat", bg="#333333", fg="white", font=("Arial", 16))
        self.title_wiindow.pack(pady=10)
        
        self.entry_channel = self.__create_input__("Canal:", tk.StringVar(value=Config.get("last_channel", "")))
        self.__create_multiple_choice__(
            'Tempo de exibição da mensagem:', 
            [("10s", 10), ("15s", 15), ("30s", 30), ("1m", 60)], 
            "message.display_time"
        )
        
        self.button_connect = tk.Button(self, text="Conectar", bg="#555555", fg="white", font=("Arial", 12), command=self.__connect__)
        self.button_connect.pack(pady=10)
        
        # self.button_change_edit = tk.Button(self, text="Editar", bg="#555555", fg="white", font=("Arial", 12), command=self.__change_edit__)
        # self.button_change_edit.pack(pady=10)
        
        self.area_info = tk.Frame(self, bg="#333333")
        self.area_info.pack(fill="x",anchor="s", side="bottom")
        
        self.label_status = tk.Label(self.area_info, text="Status: Desconectado", bg="#333333", fg="white", font=("Arial", 10))
        self.label_status.pack(padx=3, pady=3, side="left")
        
        self.label_memory = tk.Label(self.area_info, text="Memória: 0 B", bg="#333333", fg="white", font=("Arial", 10))
        self.label_memory.pack(padx=3, pady=3, side="right")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.chat = ChatWindow(self)
        self._tw_connect = None
        
    def __create_input__(self, title, textvariable):
        area_input = tk.Frame(self, bg="#333333")
        area_input.pack(fill="x", padx=20, pady=5)
        label = tk.Label(area_input, text=title, bg="#333333", fg="white", font=("Arial", 12))
        label.pack(anchor="w",side="left")
        input = tk.Entry(area_input,bg="#555555", fg="white",bd=1, font=("Arial", 12), textvariable=textvariable)
        input.pack(anchor="w",side="left", fill="x")
        return input;
    
    def __create_multiple_choice__(self, title, options = [], name_variable_config=""):
        area_choice = tk.Frame(self, bg="#333333")
        area_choice.pack(fill="x", padx=20, pady=5)
        label = tk.Label(area_choice, text=title, bg="#333333", fg="white", font=("Arial", 12))
        label.pack(anchor="w")
        
        # pegar valor do config
        value = Config.get(name_variable_config, options[0][1])
        
        var = tk.IntVar()
        var.set(value)
        
        def change_value():
            Config.set(name_variable_config, var.get())
        for option,v in options:
            rb = tk.Radiobutton(area_choice, text=option, variable=var, value=v, bg="#333333", fg="white", font=("Arial", 12), selectcolor="#555555",command=change_value)
            rb.pack(anchor="w",side="left")
        return None;
        
    def __connect__(self):
        self.button_connect.config(state=tk.DISABLED)
        channel = self.entry_channel.get()
        channel = channel.strip().lower()
        if len(channel) == 0:
            self.button_connect.config(state=tk.NORMAL, text="Conectar")
            messagebox.showinfo("Aviso", "Por favor, insira um canal.")
            return
        
        Config.set("last_channel", channel)
        
        self.connected = not self.connected
        
        if self.connected:
            if self._tw_connect is not None:
                self._tw_connect.stop()
            try:
                self._tw_connect = TwitchConnection(channel)
            except ChannelNotFoundError:
                messagebox.showinfo("Erro", "Canal não encontrado.")
                self.connected = False
                self.button_connect.config(state=tk.NORMAL, text="Conectar")
                return
            
            self.entry_channel.config(state=tk.DISABLED)
            self.button_connect.config(state=tk.NORMAL, text="Desconectar")
            
            self._tw_connect.on_message(self.__get_message__)
            self._tw_connect.on_change_status(self.__change_status__)
            self._tw_connect.start()
        else:
            if self._tw_connect is not None:
                self._tw_connect.stop()
            print("Desconectado.")
            self.entry_channel.config(state=tk.NORMAL)
            self.button_connect.config(state=tk.NORMAL, text="Conectar")
        
        self.chat.change_fixed(self.connected)
            
    def __change_edit__(self):
        self.chat.change_fixed(self.connected)
     
    def __get_message__(self, msg):
        m = Message(msg)
        self.chat.add_message(m)
        
    def __change_status__(self, new_status):
        self.label_status.config(text=f"Status: {new_status}")
        
    def on_closing(self):
        if self._tw_connect is not None:
            self._tw_connect.stop()
        self.destroy()
            
if __name__ == "__main__":
    app = ConfigWindow()
    app.mainloop()