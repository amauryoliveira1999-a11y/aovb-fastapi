import json, os

class MemoryManager:
    def __init__(self, file_path='memory.json'):
        self.memory_file = file_path
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump([], f)

    def load_memories(self):
        with open(self.memory_file, 'r') as f:
            return json.load(f)

    def save_memory(self, entry):
        memories = self.load_memories()
        memories.append({"entry": entry})
        with open(self.memory_file, 'w') as f:
            json.dump(memories, f, indent=2)
