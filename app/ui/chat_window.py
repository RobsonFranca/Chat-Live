import queue
import tkinter as tk

from app.cache.config import Config
from app.cache.emote_factory import EmoteFactory
from app.twitch.message import Message

class ChatWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.__get_config__()
        
        self.geometry(f"{self._config_geometry['width']}x{self._config_geometry['height']}+{self._config_geometry['x']}+{self._config_geometry['y']}")
        self.configure(bg="#ff00ff")
        self.wm_attributes("-transparentcolor", "#ff00ff")
        self.wm_attributes('-toolwindow', True)
        self.wm_attributes("-topmost", True)
        self.overrideredirect(True)
        
        self.container_chat = tk.Frame(self, bg="#ff00ff")
        self.container_chat.pack(fill="both", expand=True)
        
        self.frame_msgs = tk.Frame(self.container_chat, bg="#ff00ff")
        self.frame_to_move = self.__get_frame_to_change__()
        
        self._after_id = None
        self._is_fixed = True
        self._resize_config = None
        self._move_config = None
        
        self.__set_content_container__()
        self.bind("<Configure>", self.__on_configure__)
        
        self.queue_messages = queue.Queue()
        self.after(500, self.__process_queue__)
        EmoteFactory.set_root(self)
        
    def __get_config__(self):
        self._config_geometry = Config.get("window.geometry", {"width": 300, "height": 400, "x": 100, "y": 100})

    def __get_frame_to_change__(self):
        frame_to_move = tk.Frame(self.container_chat, bg="#444444", cursor="fleur")
        
        frame_to_move.bind("<Button-1>", self.__start_movement__)
        frame_to_move.bind("<B1-Motion>", self.__update_movement__)
        frame_to_move.bind("<ButtonRelease-1>", self.__finalize_movement__)
        
        wiidth_size = 5
        bottom_bar = tk.Frame(frame_to_move, height=wiidth_size, bg="#333333", cursor="sb_v_double_arrow")
        top_bar = tk.Frame(frame_to_move, height=wiidth_size, bg="#333333", cursor="sb_v_double_arrow")
        left_bar = tk.Frame(frame_to_move, width=wiidth_size, bg="#333333", cursor="sb_h_double_arrow")
        right_bar = tk.Frame(frame_to_move, width=wiidth_size, bg="#333333", cursor="sb_h_double_arrow")
        
        bottom_bar.pack(side="bottom", fill="x")
        top_bar.pack(side="top", fill="x")
        left_bar.pack(side="left", fill="y")
        right_bar.pack(side="right", fill="y")
        
        bottom_bar.resize_edge = "bottom"
        top_bar.resize_edge = "top"
        left_bar.resize_edge = "left"
        right_bar.resize_edge = "right"
        
        corner_size = 12
        tl = tk.Frame(frame_to_move, width=corner_size, height=corner_size, bg="#333333", cursor="size_nw_se")
        tr = tk.Frame(frame_to_move, width=corner_size, height=corner_size, bg="#333333", cursor="size_ne_sw")
        bl = tk.Frame(frame_to_move, width=corner_size, height=corner_size, bg="#333333", cursor="size_ne_sw")
        br = tk.Frame(frame_to_move, width=corner_size, height=corner_size, bg="#333333", cursor="size_nw_se")

        tl.place(x=0, y=0, anchor="nw")
        tr.place(relx=1.0, x=0, y=0, anchor="ne")
        bl.place(x=0, rely=1.0, anchor="sw")
        br.place(relx=1.0, rely=1.0, anchor="se")

        tl.resize_edge = "top_left"
        tr.resize_edge = "top_right"
        bl.resize_edge = "bottom_left"
        br.resize_edge = "bottom_right"
        
        bottom_bar.bind("<Button-1>", self.__start_resizing__)
        bottom_bar.bind("<B1-Motion>", self.__update_resizing__)
        bottom_bar.bind("<ButtonRelease-1>", self.__finalize_resizing__)

        top_bar.bind("<Button-1>", self.__start_resizing__)
        top_bar.bind("<B1-Motion>", self.__update_resizing__)
        top_bar.bind("<ButtonRelease-1>", self.__finalize_resizing__)

        left_bar.bind("<Button-1>", self.__start_resizing__)
        left_bar.bind("<B1-Motion>", self.__update_resizing__)
        left_bar.bind("<ButtonRelease-1>", self.__finalize_resizing__)

        right_bar.bind("<Button-1>", self.__start_resizing__)
        right_bar.bind("<B1-Motion>", self.__update_resizing__)
        right_bar.bind("<ButtonRelease-1>", self.__finalize_resizing__)

        tl.bind("<Button-1>", self.__start_resizing__)
        tl.bind("<B1-Motion>", self.__update_resizing__)
        tl.bind("<ButtonRelease-1>", self.__finalize_resizing__)

        tr.bind("<Button-1>", self.__start_resizing__)
        tr.bind("<B1-Motion>", self.__update_resizing__)
        tr.bind("<ButtonRelease-1>", self.__finalize_resizing__)

        bl.bind("<Button-1>", self.__start_resizing__)
        bl.bind("<B1-Motion>", self.__update_resizing__)
        bl.bind("<ButtonRelease-1>", self.__finalize_resizing__)

        br.bind("<Button-1>", self.__start_resizing__)
        br.bind("<B1-Motion>", self.__update_resizing__)
        br.bind("<ButtonRelease-1>", self.__finalize_resizing__)
        
        return frame_to_move

    def __set_content_container__(self):
        if self._is_fixed:
            self.frame_to_move.pack_forget()
            self.frame_msgs.pack(side="bottom", fill="x", padx=5, pady=5)
        else:
            self.frame_msgs.pack_forget()
            self.frame_to_move.pack(expand=True, fill="both")
            while len(self.frame_msgs.winfo_children()) > 0:
                self.frame_msgs.winfo_children()[0].destroy()

    def __trim_messages__(self):
        self.frame_msgs.update_idletasks()
        def get_total_height():
            total = 0
            for child in self.frame_msgs.winfo_children():
                total += child.winfo_height()+(Message.GAP_VALUE*2)
            return total

        max_height = self.container_chat.winfo_height()-50
        total = get_total_height()

        while max_height < total and len(self.frame_msgs.winfo_children()) > 0:
            child = self.frame_msgs.winfo_children()[0]
            total -= child.winfo_height()+(Message.GAP_VALUE*2)
            child.destroy()

    def __process_queue__(self):
        self.wm_attributes("-topmost", True)
        while not self.queue_messages.empty():
            mensagem = self.queue_messages.get()
            mensagem.create_tk(self.frame_msgs)
            self.__trim_messages__()
        self.after(500, self.__process_queue__)

    def add_message(self, mensagem):
        self.queue_messages.put(mensagem)
        
    def change_fixed(self, fixed):
        self._is_fixed = fixed
        self.__set_content_container__()
        
    def run(self):
        self.mainloop()
        
    def __on_configure__(self, event):
        if self._after_id is not None:
            self.after_cancel(self._after_id)

        self._after_id = self.after(300, self.__save_configs__)

    def __save_configs__(self):
        x = self.winfo_x()
        y = self.winfo_y()
        w = self.winfo_width()
        h = self.winfo_height()
        
        if(x != self._config_geometry["x"] or y != self._config_geometry["y"] or w != self._config_geometry["width"] or h != self._config_geometry["height"]):
            Config.set("window.geometry.x", x)
            Config.set("window.geometry.y", y)
            Config.set("window.geometry.width", w)
            Config.set("window.geometry.height", h)
            self.__get_config__()
            Config.save_config()
        
    def __start_resizing__(self, event):
        edge = getattr(event.widget, "resize_edge", None)
        self._resize_config = {
            "edge": edge,
            "start_x_root": event.x_root,
            "start_y_root": event.y_root,
            "init_x": self.winfo_x(),
            "init_y": self.winfo_y(),
            "init_w": self.winfo_width(),
            "init_h": self.winfo_height(),
        }

    def __update_resizing__(self, event):
        cfg = self._resize_config
        if not cfg:
            return

        dx = event.x_root - cfg["start_x_root"]
        dy = event.y_root - cfg["start_y_root"]

        edge = cfg.get("edge")
        init_x = cfg["init_x"]
        init_y = cfg["init_y"]
        init_w = cfg["init_w"]
        init_h = cfg["init_h"]

        min_w = 200
        min_h = 350

        new_x, new_y, new_w, new_h = init_x, init_y, init_w, init_h

        if edge == "bottom":
            intended_h = init_h + dy
            new_h = max(min_h, intended_h)
        elif edge == "top":
            intended_h = init_h - dy
            new_h = max(min_h, intended_h)
            delta_h = init_h - new_h
            new_y = init_y + delta_h
        elif edge == "right":
            intended_w = init_w + dx
            new_w = max(min_w, intended_w)
        elif edge == "left":
            intended_w = init_w - dx
            new_w = max(min_w, intended_w)
            delta_w = init_w - new_w
            new_x = init_x + delta_w
        elif edge == "bottom_right":
            intended_w = init_w + dx
            intended_h = init_h + dy
            new_w = max(min_w, intended_w)
            new_h = max(min_h, intended_h)
        elif edge == "bottom_left":
            intended_w = init_w - dx
            intended_h = init_h + dy
            new_w = max(min_w, intended_w)
            delta_w = init_w - new_w
            new_x = init_x + delta_w
            new_h = max(min_h, intended_h)
        elif edge == "top_right":
            intended_w = init_w + dx
            intended_h = init_h - dy
            new_w = max(min_w, intended_w)
            new_h = max(min_h, intended_h)
            delta_h = init_h - new_h
            new_y = init_y + delta_h
        elif edge == "top_left":
            intended_w = init_w - dx
            intended_h = init_h - dy
            new_w = max(min_w, intended_w)
            delta_w = init_w - new_w
            new_x = init_x + delta_w
            new_h = max(min_h, intended_h)
            delta_h = init_h - new_h
            new_y = init_y + delta_h

        self.geometry(f"{new_w}x{new_h}+{new_x}+{new_y}")

    def __finalize_resizing__(self, event):
        self._resize_config = None
        
    def __start_movement__(self, event):
        # evita iniciar movimento quando o clique veio de um grip de redimensionamento
        if event.widget is not self.frame_to_move:
            return
        # armazena posição inicial em coordenadas de tela para movimentos mais previsíveis
        self._move_config = {
            "start_x_root": event.x_root,
            "start_y_root": event.y_root,
            "init_x": self.winfo_x(),
            "init_y": self.winfo_y(),
        }

    def __update_movement__(self, event):
        if self._resize_config is not None:
            return

        cfg = self._move_config
        if not cfg:
            return

        dx = event.x_root - cfg["start_x_root"]
        dy = event.y_root - cfg["start_y_root"]

        new_x = cfg["init_x"] + dx
        new_y = cfg["init_y"] + dy

        w = self.winfo_width()
        h = self.winfo_height()

        self.geometry(f"{w}x{h}+{new_x}+{new_y}")
        
    def __finalize_movement__(self, event):
        self._move_config = None