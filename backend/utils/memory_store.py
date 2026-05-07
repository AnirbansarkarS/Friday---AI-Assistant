import json
import os

class MemoryStore:
    def __init__(self, filename="data/memory.json"):
        self.filename = filename
        self._ensure_file()
        
    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({"user_name": "User", "facts": [], "past_moods": []}, f)
                
    def load(self):
        with open(self.filename, 'r') as f:
            return json.load(f)
            
    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
            
    def update_user_name(self, name):
        data = self.load()
        data["user_name"] = name
        self.save(data)
        
    def add_fact(self, fact):
        data = self.load()
        data["facts"].append(fact)
        self.save(data)
        
    def add_mood(self, mood):
        data = self.load()
        data["past_moods"].append(mood)
        # Keep last 10 moods
        if len(data["past_moods"]) > 10:
            data["past_moods"] = data["past_moods"][-10:]
        self.save(data)
