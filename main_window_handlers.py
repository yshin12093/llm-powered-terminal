#!/usr/bin/env python3
from llm_thread import LLMThread
from message_handlers import MessageHandlers

class MainWindowHandlers:
    """
    Main handler setup for the MainWindow class
    This class coordinates the setup of all handlers for the main window
    """
    
    @staticmethod
    def setup_handlers(window):
        """
        Set up all the handlers for the main window
        
        Args:
            window: The MainWindow instance
        """
        # Set up message handlers
        MessageHandlers.setup_handlers(window)
        
        # No additional handlers needed
    

