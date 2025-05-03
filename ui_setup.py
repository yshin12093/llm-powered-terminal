#!/usr/bin/env python3
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PySide6.QtCore import Qt
from ui_controls import UIControls
from ui_components import ChatWindow, TerminalOutput

class UISetup:
    """
    Handles the UI setup for the main window
    """
    
    @staticmethod
    def setup_ui(window):
        """
        Set up the UI components for the main window
        
        Args:
            window: The MainWindow instance
        """
        # Create the central widget
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        
        # Create the main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Set up the chat and terminal components
        UISetup._setup_main_components(window, main_layout)
        
        # Set up the input controls
        UISetup._setup_input_controls(window, main_layout)
    
    @staticmethod
    def _setup_main_components(window, main_layout):
        """Set up the main components (chat window and terminal output)"""
        # Create a splitter for chat and terminal
        splitter = QSplitter(Qt.Horizontal)
        
        # Create the chat window
        window.chat_window = ChatWindow()
        splitter.addWidget(window.chat_window)
        
        # Create the terminal output
        window.terminal_output = TerminalOutput()
        splitter.addWidget(window.terminal_output)
        
        # Set the initial sizes
        splitter.setSizes([400, 400])
        
        # Add the splitter to the main layout
        main_layout.addWidget(splitter, 1)
        
    @staticmethod
    def _setup_input_controls(window, main_layout):
        """Set up the input controls (message input, send button, file button)"""
        # Create the input layout
        input_layout = QHBoxLayout()
        
        # Create the message input and send button
        window.message_input, window.send_button = UIControls.create_input_controls()
        input_layout.addWidget(window.message_input)
        input_layout.addWidget(window.send_button)
        
        # Add the input layout to the main layout
        main_layout.addLayout(input_layout)
