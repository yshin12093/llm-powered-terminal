#!/usr/bin/env python3
import re
import ollama
from PySide6.QtCore import QThread, Signal

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
        direct_command = self.check_direct_command()
        if direct_command:
            self.command_ready.emit(direct_command)
            # Don't emit a response, let the command handler do it
            return
            
        try:
            # Prepare system message
            system_message = {
                "role": "system", 
                "content": (
                    "You are a terminal assistant. Follow these rules EXACTLY:\n\n"
                    "1. Your primary role is to help users execute terminal commands.\n"
                    "2. For ANY request that can be solved with a terminal command, respond with ONLY that command.\n"
                    "3. Put ALL commands in backticks like `command`.\n"
                    "4. Be extremely concise - users want commands, not explanations.\n"
                    "5. If you see an error, suggest a fix.\n"
                    "6. Only provide explanations when the user explicitly asks for them.\n"
                    "7. For complex tasks requiring multiple commands, use && to chain them.\n\n"
                    "Examples of good responses:\n"
                    "- User: 'list files' → You: `ls`\n"
                    "- User: 'make directory test' → You: `mkdir test`\n"
                    "- User: 'find all python files' → You: `find . -name \"*.py\"`\n"
                    "- User: 'show disk usage' → You: `df -h`\n"
                    "- User: 'count lines in file.txt' → You: `wc -l file.txt`"
                )
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
            
    def check_direct_command(self):
        """Check if the user message is a direct command or can be directly mapped to a command"""
        message = self.message.strip().lower()
        
        # Handle directory navigation commands
        # Common phrases for changing directory
        cd_phrases = [
            "move to", "go to", "change to", "navigate to", "switch to", 
            "cd to", "change directory to", "move into", "go into", "enter"
        ]
        
        # Check for directory navigation phrases
        for phrase in cd_phrases:
            if message.startswith(phrase):
                # Extract the directory name
                dir_name = message[len(phrase):].strip()
                # Remove quotes if present
                dir_name = dir_name.strip('"').strip("'").strip()
                if dir_name:
                    return f"cd {dir_name}"
        
        # Simple command mappings
        command_mappings = {
            'list': 'ls',
            'list files': 'ls',
            'show files': 'ls',
            'list directory': 'ls',
            'make directory': 'mkdir',
            'create directory': 'mkdir',
            'remove': 'rm',
            'delete': 'rm',
            'copy': 'cp',
            'move file': 'mv',  # Changed from 'move' to 'move file' to avoid conflict with 'move to'
            'rename': 'mv',
            'create file': 'touch',
            'show file': 'cat',
            'display file': 'cat',
            'search': 'grep',
            'find text': 'grep',
            'find files': 'find',
            'change permissions': 'chmod',
            'change owner': 'chown',
            'current directory': 'pwd',
            'where am i': 'pwd',
            'show current directory': 'pwd',  # Added for the 'show me current directory' command
            'show working directory': 'pwd',
            'processes': 'ps aux',
            'disk usage': 'df -h',
            'directory size': 'du -h',
            'compress': 'tar -czvf',
            'extract': 'tar -xzvf',
            'download': 'wget',
            'fetch': 'curl',
            'clear screen': 'clear',
            'command history': 'history',
            'help': 'man',
            'count lines': 'wc -l',
            'count words': 'wc -w',
            'count characters': 'wc -m',
            'sort text': 'sort',
            'unique lines': 'uniq',
            'first lines': 'head',
            'last lines': 'tail',
            'current user': 'whoami',
            'current date': 'date',
            'calendar': 'cal',
            'system uptime': 'uptime',
            'system info': 'uname -a'
        }
        
        # Check for exact matches in natural language commands
        message_lower = message.lower()
        if message_lower in command_mappings:
            return command_mappings[message_lower]
        
        # If the message is an actual terminal command, just execute it directly
        common_commands = [
            'ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'touch', 'cat', 'echo', 'grep',
            'find', 'chmod', 'chown', 'pwd', 'ps', 'top', 'df', 'du', 'tar', 'zip',
            'unzip', 'ssh', 'scp', 'rsync', 'curl', 'wget', 'git', 'python', 'pip',
            'npm', 'node', 'clear', 'history', 'man', 'which', 'whereis', 'locate',
            'wc', 'sort', 'uniq', 'head', 'tail', 'less', 'more', 'nano', 'vim',
            'sudo', 'su', 'whoami', 'who', 'date', 'cal', 'uptime', 'uname'
        ]
        
        # Check if the message starts with a common command
        if any(message.startswith(cmd) for cmd in common_commands):
            return self.message.strip()  # Return original message with case preserved
            
        # Direct command mapping for common natural language requests
        direct_commands = {
            "ls": "ls",
            "list files": "ls",
            "list directory": "ls",
            "show files": "ls",
            "pwd": "pwd",
            "current directory": "pwd",
            "where am i": "pwd",
            "clear": "clear",
            "clear screen": "clear",
            "show disk usage": "df -h",
            "show memory usage": "free -h",
            "show processes": "ps aux",
            "show date": "date",
            "show calendar": "cal",
            "show uptime": "uptime",
            "who am i": "whoami",
        }
        
        # Check for exact matches in natural language commands
        message_lower = message.lower()
        if message_lower in direct_commands:
            return direct_commands[message_lower]
        
        # Handle common patterns
        patterns = {
            # Directory operations
            r"make (?:a )?(?:new )?directory (?:called |named )?['\"]?([\w\-\.]+)['\"]?": "mkdir {}",
            r"create (?:a )?(?:new )?directory (?:called |named )?['\"]?([\w\-\.]+)['\"]?": "mkdir {}",
            
            # File operations
            r"make (?:a )?(?:new )?file (?:called |named )?['\"]?([\w\-\.]+)['\"]?": "touch {}",
            r"create (?:a )?(?:new )?file (?:called |named )?['\"]?([\w\-\.]+)['\"]?": "touch {}",
            r"show (?:contents of |the )?file ['\"]?([\w\-\.]+)['\"]?": "cat {}",
            
            # Search operations
            r"find (?:all )?files (?:with |containing )?['\"]?([\w\-\.]+)['\"]?": "find . -name \"*{}*\"",
            r"search for ['\"]?([\w\-\.]+)['\"]? in files": "grep -r \"{}\" .",
            
            # Count operations
            r"count (?:lines in |words in )?(?:file )?['\"]?([\w\-\.]+)['\"]?": "wc {}",
        }
        
        for pattern, cmd_template in patterns.items():
            match = re.search(pattern, message_lower)
            if match:
                param = match.group(1)
                return cmd_template.format(param)
                
        return None
