#!/usr/bin/env python3
import sys
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow
import ollama

# Import custom modules
from memory_manager import MemoryManager
from file_analyzer import FileAnalyzer
from main_window_handlers import MainWindowHandlers
from ui_setup import UISetup

# Load environment variables
load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Check if Ollama is available and has the llama3 model
        try:
            models = ollama.list()
            # The response is a ListResponse object with a models attribute
            llama3_available = any("llama3" in model.model for model in models.models)
            if not llama3_available:
                print("Warning: llama3 model not found in Ollama. Please run 'ollama pull llama3'")
        except Exception as e:
            print(f"Error connecting to Ollama: {str(e)}")
            print("Please make sure Ollama is installed and running")
            sys.exit(1)
        
        # Initialize components
        self.memory_manager = MemoryManager()
        self.file_analyzer = FileAnalyzer()
        
        # Set up window properties
        self.setWindowTitle("LLM-Powered Terminal")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: #f0f0f0;")
        
        # Set up event handlers first - this will define all the handler methods
        MainWindowHandlers.setup_handlers(self)
        
        # Now set up UI - this will connect signals to the handlers
        UISetup.setup_ui(self)
        
        # Connect file analyzer signal
        self.file_analyzer.analysis_complete.connect(self.handle_file_analysis)
        
        # Track active threads
        self.active_threads = []
        
        # Show welcome message
        self.chat_window.add_message("Assistant", "Welcome to LLM-Powered Terminal using Ollama with Llama 3.\n\nHow can I help you today?")
        
    def closeEvent(self, event):
        """Clean up threads when the application is closed"""
        # Wait for all threads to finish
        for thread in self.active_threads:
            if thread.isRunning():
                thread.quit()
                thread.wait(1000)  # Wait up to 1 second for thread to finish
        
        # Accept the close event
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
