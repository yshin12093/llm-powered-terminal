#!/usr/bin/env python3
import re
from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QFont, QTextCursor

class ChatWindow(QTextEdit):
    """Custom QTextEdit for the chat window with plain text formatting"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Menlo", 22))  # Increased from 11 to 22 (2x larger)
        self.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0;")
        self.setAcceptRichText(False)  # Use plain text
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
    def add_message(self, sender, message):
        """
        Add a message to the chat window with plain text formatting
        
        Args:
            sender: The sender of the message (User, Assistant, or System)
            message: The message content
        """
        # Simplify sender display - only show "You" or "Assistant"
        display_sender = sender
        if sender == "System":
            display_sender = "Assistant"
            
        # Format the message with proper line breaks
        if self.toPlainText():  # If there's already content
            formatted_message = f"\n{display_sender}: {message}"
        else:
            # First message doesn't need leading newline
            formatted_message = f"{display_sender}:{message}"
        
        # Add the message to the chat window
        self.append(formatted_message)
        
        # Scroll to the bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class TerminalOutput(QTextEdit):
    """Custom QTextEdit for terminal output"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Menlo", 20))  # Increased from 10 to 20 (2x larger)
        self.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0;")
        
    def add_output(self, command, output, exit_code):
        import os
        import getpass
        from pathlib import Path
        from terminal_executor import WorkingDirectory
        
        try:
            # Get current username and directory for the prompt
            username = getpass.getuser()
            current_dir = WorkingDirectory.get_dir()
            dir_name = Path(current_dir).name
            
            # Create the prompt string
            prompt = f"\n{username}@{os.uname().nodename} {dir_name} % {command}\n"
            
            # Add the command with prompt
            self.append(prompt)
            
            # Add the output
            if output:
                self.append(output)
            
            # Scroll to the bottom
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        except Exception as e:
            print(f"Error in terminal output: {str(e)}")
