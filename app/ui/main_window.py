import os
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import psutil

from app.cache.config import Config
from app.twitch.connection import ChannelNotFoundError, TwitchConnection
from app.ui.chat_window import ChatWindow
from app.twitch.message import Message
from app.ui.fullscreen import Fullscreen

class MainWindow(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Chat Live - Configurações")
        self.geometry("400x400")
        self.configure(bg="#333333")
        self.wm_attributes("-topmost", True)
        self.resizable(width=False, height=False)
        
        self.chat = ChatWindow(self)
        self.fullscreen = Fullscreen(self)
        self._tw_connect = None
        
        self.commands = {
            "!olha_o_sonic": self.fullscreen.create_sonic,
            "!vibrar":       self.fullscreen.shake_screen,
            "!aplauso":      self.fullscreen.create_applause,
        }
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.__construct_window__()
        
        self.connected = False
        self.chat.change_fixed(self.connected)
        self.last_command_time = 0
        
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
    
    def __frame_init__(self):
        frame = tk.Frame(self.notebook, bg="#333333")
        channel_label = tk.Label(frame, text="Canal", bg="#333333", fg="white", font=("Arial", 12, "bold"))
        channel_label.pack(padx=20, pady=6, anchor="w")
        self.entry_channel = self.__create_input__(frame, "Canal:", tk.StringVar(value=Config.get("last_channel", "")))
        
        self.button_connect = tk.Button(frame, text="Conectar", bg="#555555", fg="white", font=("Arial", 12), command=self.__connect__)
        self.button_connect.pack(pady=10)
        
        self.notebook.add(frame, text="Main")
        
    def __frame_config__(self):
        frame = tk.Frame(self.notebook, bg="#333333")
        message_label = tk.Label(frame, text="Mensagens", bg="#333333", fg="white", font=("Arial", 12, "bold"))
        message_label.pack(padx=20, pady=6, anchor="w")
        self.__create_multiple_choice__(
            frame,
            'Tempo de exibição da mensagem:', 
            [("10s", 10), ("15s", 15), ("30s", 30), ("1m", 60)], 
            "message.display_time"
        )
        self.__create_select__(
            frame,
            "Fonte da mensagem:",
            ["Segoe UI", "Arial", "Times New Roman", "Comic Sans MS"],
            "message.font"
        )
        self.__create_select__(
            frame,
            "Tamanho da fonte:",
            ["8", "10", "12", "14"],
            "message.font_size"
        )
        self.__create_multiple_choice__(
            frame,
            'Salvar emotes:', 
            [("Sim", True), ("Não", False)], 
            "emote.save_emotes"
        )
        
        self.notebook.add(frame, text="Configurações")
        
    def __frame_commands__(self):
        frame = tk.Frame(self.notebook, bg="#333333")
        message_label = tk.Label(frame, text="Comandos", bg="#333333", fg="white", font=("Arial", 12, "bold"))
        message_label.pack(padx=20, pady=6, anchor="w")
        
        self.__create_multiple_choice__(
            frame,
            'Modifica o tempo de recarga:', 
            [("1m", 1), ("3m", 3), ("5m", 5), ("10m", 10), ("15m", 15)], 
            "command.cooldown"
        )
        
        grid = tk.Frame(frame, bg="#333333")
        grid.pack(anchor="n", expand=True, fill="x", padx=10)
        row = 0
        for command, funct in self.commands.items():
            label = tk.Label(grid, text=command, bg="#333333", fg="white", font=("Arial", 12, "bold"))
            btn = tk.Button(grid, text="Play", command=funct)
            label.grid(row=row, column=0, sticky="w", padx=10)
            btn.grid(row=row, column=1,  sticky="e")
            row+=1
            
        self.notebook.add(frame, text="Comandos")
        
    def __construct_window__(self):
        self.__frame_init__()
        self.__frame_config__()
        self.__frame_commands__()
        
        self.area_info = tk.Frame(self, bg="#333333")
        self.area_info.pack(fill="x",anchor="s", side="bottom")
        
        self.label_status = tk.Label(self.area_info, text="Status: Desconectado", bg="#333333", fg="white", font=("Arial", 10))
        self.label_status.pack(padx=3, pady=3, side="left")
        
        self.label_memory = tk.Label(self.area_info, text="Memória: 0 B", bg="#333333", fg="white", font=("Arial", 10))
        self.label_memory.pack(padx=3, pady=3, side="right")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def __create_input__(self, master, title, textvariable):
        area_input = tk.Frame(master, bg="#333333")
        area_input.pack(fill="x", padx=20, pady=5)
        label = tk.Label(area_input, text=title, bg="#333333", fg="white", font=("Arial", 12))
        label.pack(anchor="w",side="left")
        input = tk.Entry(area_input,bg="#555555", fg="white",bd=1, font=("Arial", 12), textvariable=textvariable)
        input.pack(anchor="w",side="left", fill="x")
        return input;
    
    def __create_select__(self, master, title, options = [], name_variable_config=""):
        area_select = tk.Frame(master, bg="#333333")
        area_select.pack(fill="x", padx=20, pady=5)
        label = tk.Label(area_select, text=title, bg="#333333", fg="white", font=("Arial", 12))
        label.pack(anchor="w",side="left")
        select = ttk.Combobox(area_select, font=("Arial", 12), values=options)
        select.pack(anchor="w",side="left", fill="x")
        
        value = Config.get(name_variable_config, options[0])
        select.current(options.index(value))
        
        def change(event):
            Config.set(name_variable_config, select.get())
            
        select.bind("<<ComboboxSelected>>", change)
        
        return select;
    
    def __create_multiple_choice__(self, master, title, options = [], name_variable_config=""):
        area_choice = tk.Frame(master, bg="#333333")
        area_choice.pack(fill="x", padx=20, pady=5)
        label = tk.Label(area_choice, text=title, bg="#333333", fg="white", font=("Arial", 12))
        label.pack(anchor="w")
        
        value = Config.get(name_variable_config, options[0][1])
        
        var = tk.IntVar()
        var.set(value)
        
        def change_value():
            Config.set(name_variable_config, var.get())
        for option,v in options:
            rb = tk.Radiobutton(area_choice, text=option, variable=var, value=v, bg="#333333", fg="white", font=("Arial", 12), selectcolor="#555555",command=change_value)
            rb.pack(anchor="w",side="left",padx=5)
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
            self.entry_channel.config(state=tk.NORMAL)
            self.button_connect.config(state=tk.NORMAL, text="Conectar")
        
        self.chat.change_fixed(self.connected)
            
    def __change_edit__(self):
        self.chat.change_fixed(self.connected)
     
    def __get_message__(self, msg):
        m = Message(msg, self.commands.keys())
        if m.is_command():
            print(m.command, time.time() - self.last_command_time, Config.get("command.cooldown", 1) * 60)
            if time.time() - self.last_command_time > Config.get("command.cooldown", 1) * 60:
                if m.command in self.commands:
                    if self.commands[m.command]():
                        self.last_command_time = time.time()
        self.chat.add_message(m)
        
    def __change_status__(self, new_status):
        self.label_status.config(text=f"Status: {new_status}")
        
    def on_closing(self):
        if self._tw_connect is not None:
            self._tw_connect.stop()
        self.destroy()
            
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()