from random import randint
import colorsys

class Color():
    def __init__(self, r, g, b):
        self.rgb = (r, g, b)
        
    def to_hex(self):
        return '#%02x%02x%02x' % self.rgb
    
    def change_brightness_hsv(self, factor):
        r, g, b = self.rgb
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        v = min(1.0, max(0.0, v * factor))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.rgb = (int(r * 255), int(g * 255), int(b * 255))
        return self
    
    def get_random():
        return Color(randint(0x11, 0xFF), randint(0x11, 0xFF), randint(0x11, 0xFF))
    
    def get_by_hex(hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return Color(r, g, b)