#!/usr/bin/env python3
from PySide6.QtWidgets import QPushButton, QLineEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class UIControls:
    """
    Handles the creation and setup of UI controls
    """
    
    @staticmethod
    def create_input_controls():
        """
        Create the input controls for the application
        
        Returns:
            tuple: (message_input, send_button)
        """
        # Create the message input
        message_input = QLineEdit()
        message_input.setPlaceholderText("Type a message or command...")
        message_input.setFont(QFont("Menlo", 18))  # Increased from 9 to 18 (2x larger)
        
        # Create the send button
        send_button = QPushButton("Send")
        send_button.setFont(QFont("Menlo", 18))  # Increased from 9 to 18 (2x larger)
        send_button.setFixedWidth(100)
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
        """)
        
        return message_input, send_button
    

