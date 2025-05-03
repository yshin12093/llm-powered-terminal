#!/usr/bin/env python3
from pathlib import Path
from PySide6.QtWidgets import QFileDialog
from llm_thread import LLMThread
from command_handlers import CommandHandlers

class MainWindowHandlers:
    """
    Handler methods for the MainWindow class
    This class contains the event handlers and business logic for the main window
    """
    
    @staticmethod
    def setup_handlers(window):
        """
        Set up all the handlers for the main window
        
        Args:
            window: The MainWindow instance
        """
        # Connect the chat and file handlers
        window.send_message = lambda: MainWindowHandlers.handle_send_message(window)
        window.handle_llm_response = lambda response: MainWindowHandlers.handle_llm_response(window, response)
        window.analyze_file_dialog = lambda: MainWindowHandlers.analyze_file_dialog(window)
        window.handle_file_analysis = lambda file_path, analysis: MainWindowHandlers.handle_file_analysis(window, file_path, analysis)
        
        # Set up command handlers
        CommandHandlers.setup_handlers(window)
    
    @staticmethod
    def handle_send_message(window):
        """Handle sending a message"""
        message = window.input_field.text().strip()
        if not message:
            return
            
        # Add user message to chat
        window.chat_window.add_message("You", message)
        
        # Clear input field
        window.input_field.clear()
        
        # Add to memory
        window.memory_manager.add_message("user", message)
        
        # Process with LLM
        window.llm_thread = LLMThread(message, window.memory_manager.get_messages())
        window.llm_thread.response_ready.connect(window.handle_llm_response)
        window.llm_thread.command_ready.connect(window.execute_command)
        window.llm_thread.finished.connect(
            lambda: window.active_threads.remove(window.llm_thread) if window.llm_thread in window.active_threads else None
        )
        
        # Add to active threads
        window.active_threads.append(window.llm_thread)
        
        # Start the thread
        window.llm_thread.start()
    
    @staticmethod
    def handle_llm_response(window, response):
        # Display assistant message
        window.chat_window.add_message("Assistant", response)
        
        # Add to memory
        window.memory_manager.add_conversation("assistant", response)
    
    @staticmethod
    def analyze_file_dialog(window):
        """Open a file dialog to select a file for analysis"""
        file_dialog = QFileDialog(window)
        file_path, _ = file_dialog.getOpenFileName(
            window,
            "Select File to Analyze",
            str(Path.home()),
            "All Files (*)"
        )
        
        if file_path:
            window.chat_window.add_message("System", f"Analyzing file: {file_path}...")
            window.file_analyzer.analyze_file(file_path)
    
    @staticmethod
    def handle_file_analysis(window, file_path, analysis):
        """Handle the completed file analysis"""
        file_name = Path(file_path).name
        window.chat_window.add_message("Assistant", f"**Analysis of {file_name}:**\n\n{analysis}")
        
        # Add to memory
        window.memory_manager.add_conversation("assistant", f"Analysis of {file_name}: {analysis}")
