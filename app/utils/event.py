class Event:
    def __init__(self):
        self.events = {}
        
    def add(self, name, callback):
        if name not in self.events:
            self.events[name] = []
        self.events[name].append(callback)
        
    def trigger(self, name, data=None):
        if name in self.events:
            for callback in self.events[name]:
                callback(data)