#!/usr/bin/env python3
import subprocess
import os
import re
from PySide6.QtCore import QThread, Signal, QObject

# Singleton to store the current working directory
class WorkingDirectory:
    _instance = None
    _current_dir = os.getcwd()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkingDirectory, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_dir(cls):
        return cls._current_dir
    
    @classmethod
    def set_dir(cls, new_dir):
        if os.path.isdir(new_dir):
            cls._current_dir = new_dir
            return True
        return False

class TerminalExecutor(QThread):
    """Thread for executing terminal commands"""
    command_output = Signal(str, int)  # Output, exit code
    
    def __init__(self, command):
        super().__init__()
        self.command = command
    
    def is_cd_command(self, command):
        """Check if the command is a cd command and extract the directory"""
        # Match cd command with various formats
        cd_pattern = r'^cd\s+([^&;|<>]*)'  # Match 'cd dir' but not if followed by &&, ;, etc.
        match = re.match(cd_pattern, command.strip())
        if match:
            return match.group(1).strip()  # Return the directory part
        return None
    
    def handle_cd_command(self, command):
        """Handle cd command by updating the working directory"""
        target_dir = self.is_cd_command(command)
        if target_dir:
            # Handle relative paths
            if not os.path.isabs(target_dir):
                full_path = os.path.join(WorkingDirectory.get_dir(), target_dir)
                full_path = os.path.normpath(full_path)
            else:
                full_path = target_dir
                
            # Try to change directory
            if os.path.isdir(full_path):
                WorkingDirectory.set_dir(full_path)
                return f"Changed directory to {full_path}\n", 0
            else:
                return f"cd: {target_dir}: No such file or directory\n", 1
        return None, None
        
    def run(self):
        try:
            # Check if this is a cd command
            output, exit_code = self.handle_cd_command(self.command)
            if output is not None and exit_code is not None:
                # This was a cd command and we handled it
                self.command_output.emit(output, exit_code)
                return
                
            # For other commands, execute in the current working directory
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
                cwd=WorkingDirectory.get_dir()  # Use the current working directory
            )
            
            output = process.communicate()[0]
            exit_code = process.returncode
            
            self.command_output.emit(output, exit_code)
        except Exception as e:
            self.command_output.emit(str(e), 1)
