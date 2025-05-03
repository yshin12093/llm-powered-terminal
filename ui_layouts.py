#!/usr/bin/env python3
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QSplitter
)
from PySide6.QtCore import Qt
from ui_components import ChatWindow, TerminalOutput

class UILayouts:
    """
    Handles the layout setup for the main window
    """
    
    @staticmethod
    def create_main_layout():
        """
        Create the main layout for the application
        
        Returns:
            tuple: (main_layout, chat_window, terminal_output, input_field)
        """
        # Create the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create the splitter for chat and terminal
        splitter = QSplitter(Qt.Horizontal)
        
        # Create the chat window
        chat_window = ChatWindow()
        splitter.addWidget(chat_window)
        
        # Create the terminal output
        terminal_output = TerminalOutput()
        splitter.addWidget(terminal_output)
        
        # Set the initial sizes
        splitter.setSizes([400, 400])
        
        # Add the splitter to the main layout
        main_layout.addWidget(splitter, 1)
        
        # Create the input layout
        input_layout = QHBoxLayout()
        
        # Create the input field
        input_field = QHBoxLayout()
        
        return main_layout, chat_window, terminal_output, input_field
    
    @staticmethod
    def create_input_layout(input_field):
        """
        Create the input layout for the application
        
        Args:
            input_field: The input field layout
            
        Returns:
            tuple: (input_layout, message_input)
        """
        # Create the input layout
        input_layout = QHBoxLayout()
        
        # Create the message input
        message_input = QLineEdit()
        message_input.setPlaceholderText("Type a message or command...")
        message_input.setFont(QFont("Menlo", 18))  # Increased from 9 to 18 (2x larger)
        
        # Add the message input to the input layout
        input_layout.addWidget(message_input)
        
        return input_layout, message_input
