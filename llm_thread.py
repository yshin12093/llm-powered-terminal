#!/usr/bin/env python3
import re
import ollama
from PySide6.QtCore import QThread, Signal
from command_parser import parse_direct_command
from llm_prompts import TERMINAL_ASSISTANT_PROMPT

class LLMThread(QThread):
    """Thread for LLM interactions"""
    response_ready = Signal(str)
    command_ready = Signal(str)
    
    def __init__(self, message, memory=None):
        super().__init__()
        self.message = message
        self.memory = memory or []
        
    def run(self):
        # Check for direct command patterns first
        direct_command = parse_direct_command(self.message)
        if direct_command:
            self.command_ready.emit(direct_command)
            # Don't emit a response, let the command handler do it
            return
            
        try:
            # Prepare system message
            system_message = {
                "role": "system", 
                "content": TERMINAL_ASSISTANT_PROMPT
            }
            
            messages = [system_message]
            
            # Add memory context
            for mem in self.memory:
                messages.append({"role": mem["role"], "content": mem["content"]})
                
            # Add the current message
            messages.append({"role": "user", "content": self.message})
            
            # Generate response using Ollama with Llama 3
            response = ollama.chat(model="llama3", messages=messages)
            
            # Extract the assistant's message
            assistant_message = response["message"]["content"]
            
            # Check if the response contains a command to execute
            # Using a simple heuristic: look for commands between backticks
            command_matches = re.findall(r'`(.*?)`', assistant_message)
            
            # Process the first command that looks like a shell command
            if command_matches:
                command = command_matches[0].strip()
                self.command_ready.emit(command)
                # Don't emit the response if it's just a command execution
                if assistant_message.strip() == f"Executing: `{command}`" or \
                   assistant_message.strip() == f"Executing:\n\n`{command}`":
                    # Skip emitting response as the command handler will do it
                    return
            
            # Emit the response for non-command or complex responses
            self.response_ready.emit(assistant_message)
            
        except Exception as e:
            self.response_ready.emit(f"Error communicating with LLM: {str(e)}")
