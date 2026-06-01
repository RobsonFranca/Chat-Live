from app.twitch.emote import Emote

class EmoteFactory:
    _emotes = {}

    def get_emotes(text_emotes: str) -> list[Emote]:
        r = []
        if len(text_emotes) == 0:
            return r
        for text_emote in text_emotes.split("/"):
            [id, positons] = text_emote.split(":",1)
            if id not in EmoteFactory._emotes:
                EmoteFactory._emotes[id] = Emote(id, positons)
            
            r.append(EmoteFactory._emotes[id])
            
        return  r
    
    def set_root(root):
        root.after(10, EmoteFactory.__annotations__, root)
        
    def __annotations__(root):
        for emote in EmoteFactory._emotes.values():
            emote.animation()
        root.after(10, EmoteFactory.__annotations__, root)