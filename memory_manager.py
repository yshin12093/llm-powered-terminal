#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

class MemoryManager:
    """Manages conversation and command history with persistence"""
    
    def __init__(self):
        self.memory_file = Path.home() / ".llm_terminal_memory.json"
        self.memory = self.load_memory()
        
    def load_memory(self):
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return {"conversations": [], "command_history": {}}
        else:
            return {"conversations": [], "command_history": {}}
    
    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f)
    
    def add_conversation(self, role, content):
        self.memory["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content
        })
        # Keep only the last 50 conversation entries
        if len(self.memory["conversations"]) > 50:
            self.memory["conversations"] = self.memory["conversations"][-50:]
        self.save_memory()
    
    def add_command_result(self, command, output, exit_code):
        self.memory["command_history"][command] = {
            "last_run": datetime.now().isoformat(),
            "output": output,
            "exit_code": exit_code,
            "run_count": self.memory["command_history"].get(command, {}).get("run_count", 0) + 1
        }
        self.save_memory()
    
    def get_recent_conversations(self, limit=10):
        # Return the most recent conversations
        return self.memory["conversations"][-limit:]
        
    def add_message(self, role, content):
        # Alias for add_conversation
        self.add_conversation(role, content)
        
    def get_messages(self, limit=10):
        # Alias for get_recent_conversations
        return self.get_recent_conversations(limit)
    
    def get_command_history(self, command=None):
        if command:
            return self.memory["command_history"].get(command)
        return self.memory["command_history"]
