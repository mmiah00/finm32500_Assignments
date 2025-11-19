from datetime import datetime
import json

class Logger:
    _instance = None

    def __init__(self, path="events.json"):
        self.path = path
        self.events = []
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def log(self, event_type, data):
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": event_type,
            "data": data
        }
        self.events.append(event)

    def save(self):
        # save to events.json 
        with open(self.path, 'w') as f:
            json.dump(self.events, f, indent=4)