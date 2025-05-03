#!/usr/bin/env python3
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSplitter, QLabel, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
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
        # Set up larger font for all UI elements
        large_font = QFont("Menlo", 18)  # Large font for UI elements
        
        # Main widget and layout
        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #1e1e1e;")
        main_layout = QVBoxLayout(main_widget)
        
        # Create a splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)
        
        # Chat section
        chat_widget = QWidget()
        chat_widget.setStyleSheet("background-color: #1e1e1e;")
        chat_layout = QVBoxLayout(chat_widget)
        
        # Chat window
        window.chat_window = ChatWindow()
        chat_layout.addWidget(window.chat_window)
        
        # Input area
        input_layout = QHBoxLayout()
        window.input_field = QLineEdit()
        window.input_field.setPlaceholderText("Ask me anything or type a command...")
        window.input_field.returnPressed.connect(window.send_message)
        window.input_field.setFont(large_font)  # Set larger font
        window.input_field.setMinimumHeight(50)  # Make input field taller
        window.input_field.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; border: 1px solid #3a3a3a;")
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(window.send_message)
        send_button.setFont(large_font)  # Set larger font
        send_button.setStyleSheet("background-color: #3a3a3a; color: #f0f0f0;")
        
        analyze_file_button = QPushButton("Analyze File")
        analyze_file_button.clicked.connect(window.analyze_file_dialog)
        analyze_file_button.setFont(large_font)  # Set larger font
        analyze_file_button.setStyleSheet("background-color: #3a3a3a; color: #f0f0f0;")
        
        input_layout.addWidget(window.input_field)
        input_layout.addWidget(send_button)
        input_layout.addWidget(analyze_file_button)
        
        chat_layout.addLayout(input_layout)
        
        # Terminal Output section
        terminal_widget = QWidget()
        terminal_widget.setStyleSheet("background-color: #1e1e1e;")
        terminal_layout = QVBoxLayout(terminal_widget)
        
        terminal_label = QLabel("Terminal Output")
        terminal_label.setFont(large_font)  # Set larger font
        terminal_label.setStyleSheet("color: #f0f0f0;")
        terminal_layout.addWidget(terminal_label)
        
        window.terminal_output = TerminalOutput()
        terminal_layout.addWidget(window.terminal_output)
        
        # Add widgets to splitter
        splitter.addWidget(chat_widget)
        splitter.addWidget(terminal_widget)
        
        # Set initial sizes (70% chat, 30% terminal)
        splitter.setSizes([int(window.height() * 0.7), int(window.height() * 0.3)])
        
        main_layout.addWidget(splitter)
        
        window.setCentralWidget(main_widget)
