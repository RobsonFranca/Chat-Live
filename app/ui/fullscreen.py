import tkinter as tk
from PIL import Image, ImageTk
import time

from app.utils.file import get_path_or_none

class Fullscreen(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.attributes("-fullscreen", True)
        self.configure(bg="#ff00ff")
        self.wm_attributes("-transparentcolor", "#ff00ff")
        self.wm_attributes("-topmost", True)
        self.overrideredirect(True)
        
    def create_sonic(self):
        sonic_path = get_path_or_none("resource.a", "gif")
        if sonic_path:
            img = Image.open(sonic_path)
            frames = []
            try:
                while True:
                    frame_tk = ImageTk.PhotoImage(img.copy().resize(img.size, Image.Resampling.LANCZOS).convert("RGBA"))
                    frames.append(frame_tk)
                    img.seek(img.tell() + 1)
            except EOFError:
                pass
            label = tk.Label(self, bg="#ff00ff", image=frames[1])
            label.place(x=-img.width, y=self.winfo_screenheight() - img.height)
            label.image = frames[1]
            label.after(10, self.after_frame, label, frames, 0, time.time(), img.info.get('duration', 100))
            
    def after_frame(self, label, frames, index, _time, delay=100):
        now = time.time()
        if now - _time >= delay / 1000:
            _time = now
            if frames:
                label.configure(image=frames[index])
                index = (index + 1) % len(frames)
        label.place(x=label.winfo_x() + 10)
        if label.winfo_x() > self.winfo_screenwidth():
            label.destroy()
        else:
            label.after(10, self.after_frame, label, frames, index, _time, delay)
        