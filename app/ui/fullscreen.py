import random
import tkinter as tk
from PIL import Image, ImageGrab, ImageTk
import time
import pygame

from app.utils.file import get_path_or_none

class Fullscreen(tk.Toplevel):
    GIFS_PATH = "resource.gifs."
    SOUNDS_PATH = "resource.sounds."
    
    def __init__(self, root):
        super().__init__(root)
        self.attributes("-fullscreen", True)
        self.configure(bg="#ff00ff")
        self.wm_attributes("-transparentcolor", "#ff00ff")
        self.wm_attributes('-toolwindow', True)
        self.wm_attributes("-topmost", True)
        self.overrideredirect(True)
        self.command_running = False
        pygame.mixer.init()
        
        #self.create_applause()
    
    def get_gif(self, path):
        img = Image.open(path)
        frames = []
        try:
            while True:
                frame_tk = ImageTk.PhotoImage(img.copy().resize(img.size, Image.Resampling.LANCZOS).convert("RGBA"))
                frames.append(frame_tk)
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        return frames, img.info.get('duration', 100), img.size
    
    def create_sonic(self):
        if self.command_running:
            return False
        
        self.command_running = True
        def after_frame(label, frames, index, _time, delay=100):
            now = time.time()
            if now - _time >= delay / 1000:
                _time = now
                if frames:
                    label.configure(image=frames[index])
                    index = (index + 1) % len(frames)
            label.place(x=label.winfo_x() + 10)
            if label.winfo_x() > self.winfo_screenwidth():
                label.destroy()
                self.command_running = False
            else:
                label.after(10, after_frame, label, frames, index, _time, delay)
                
        self.wm_attributes("-topmost", True)
        sonic_path = get_path_or_none(Fullscreen.GIFS_PATH + "a", "gif")
        if sonic_path:
            frames, delay, size = self.get_gif(sonic_path)
            label = tk.Label(self, bg="#ff00ff", image=frames[1])
            label.place(x=-size[0], y=self.winfo_screenheight() - size[1])
            label.image = frames[1]
            label.after(10, after_frame, label, frames, 0, time.time(), delay)
            
        return True
       
    def shake_screen(self):
        if self.command_running:
            return False
        
        self.command_running = True
        def shake(index, positions, base_x, base_y, start_time, duration):
            elapsed = (time.time() - start_time) * 1000
            if elapsed >= duration:
                label.destroy()
                self.command_running = False
                return

            dx, dy = positions[index]
            label.place(x=base_x + dx, y=base_y + dy)
            next_index = (index + 1) % len(positions)
            label.after(1, shake, next_index, positions, base_x, base_y, start_time, duration)

        self.wm_attributes("-topmost", True)
        print_memoria = ImageGrab.grab()
        foto_tkinter = ImageTk.PhotoImage(print_memoria)
        label = tk.Label(self, image=foto_tkinter, bg="#000000")
        label.image = foto_tkinter
        base_x, base_y = -2, -2
        label.place(x=base_x, y=base_y)

        positions = [
            (-6, 0), (6, 0), (0, -6), (0, 6),
            (-4, 4), (4, -4), (-3, 3), (3, -3)
        ]

        shake(0, positions, base_x, base_y, time.time(), 1000)
        return True
    
    def create_applause(self):
        if self.command_running:
            return False
        
        self.command_running = True
        COUNT_MAX = 10
        def after_frame(label, sound, frames, index, _time, delay, start_time, duration, i):
            now = time.time()
            if now - _time >= delay / 1000:
                _time = now
                if frames:
                    label.configure(image=frames[index])
                    index = (index + 1) % len(frames)
            if now  - start_time >= duration / 1000:
                label.destroy()
                try:
                    sound.stop()
                except AttributeError:
                    pass
                if i >= COUNT_MAX-1:
                    self.command_running = False
            else:
                label.after(10, after_frame, label, sound, frames, index, _time, delay, start_time, duration, i)
                
        self.wm_attributes("-topmost", True)
        
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        cols = max(1, screen_w // 128)
        rows = max(1, screen_h // 128)
        step_x = screen_w // cols
        step_y = screen_h // rows
        cell_positions = [(x * step_x, y * step_y) for y in range(rows) for x in range(cols)]
        
        applause1_path = get_path_or_none(Fullscreen.GIFS_PATH + "b1", "gif")
        applause2_path = get_path_or_none(Fullscreen.GIFS_PATH + "b2", "gif")
        sound_path = get_path_or_none(Fullscreen.SOUNDS_PATH + "b", "mp3")
        if applause1_path and applause2_path:
            frames1, delay1, size1 = self.get_gif(applause1_path)
            frames2, delay2, size2 = self.get_gif(applause2_path)
            frames_list = [frames1, frames2]
            random.shuffle(cell_positions)
            available_positions = cell_positions[:min(len(cell_positions), 25)]

            def spawn_applause(i):
                if i >= COUNT_MAX or not available_positions:
                    return
                x, y = available_positions.pop()
                index = random.randint(0, len(frames_list) - 1)
                frames = frames_list[index]
                label = tk.Label(self, bg="#ff00ff", image=frames[0])
                label.image = frames[0]
                label.place(x=x, y=y)
                sound = pygame.mixer.Sound(sound_path).play()
                label.after(10, after_frame, label, sound, frames, 0, time.time(), [delay1, delay2][index], time.time(), 3000, i)

                label.after(random.randint(10, 300), spawn_applause, i + 1)
                
            spawn_applause(0)
            
        return True