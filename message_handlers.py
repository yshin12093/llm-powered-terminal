#!/usr/bin/env python3
from llm_thread import LLMThread
from command_handlers import CommandHandlers

class MessageHandlers:
    """
    Handlers for message-related functionality
    """
    
    @staticmethod
    def setup_handlers(window):
        """
        Set up the message-related handlers for the main window
        
        Args:
            window: The MainWindow instance
        """
        # Add handler methods to the window first
        window.handle_send_message = lambda: MessageHandlers.handle_send_message(window)
        window.handle_llm_response = lambda response: MessageHandlers.handle_llm_response(window, response)
        window.handle_command = lambda command: MessageHandlers.handle_command(window, command)
        
        # Now connect UI signals to the handlers
        window.message_input.returnPressed.connect(window.handle_send_message)
        window.send_button.clicked.connect(window.handle_send_message)
        
        # Set up command handlers
        CommandHandlers.setup_handlers(window)
    
    @staticmethod
    def handle_send_message(window):
        """Handle sending a message from the input field"""
        # Get the message from the input field
        message = window.message_input.text().strip()
        if not message:
            return
            
        # Clear the input field
        window.message_input.clear()
        
        # Add the message to the chat window
        window.chat_window.add_message("You", message)
        
        # Add to memory
        window.memory_manager.add_message("user", message)
        
        # Create a thread to process the message with the LLM
        llm_thread = LLMThread(message, window.memory_manager.get_messages())
        llm_thread.response_ready.connect(window.handle_llm_response)
        llm_thread.command_ready.connect(window.handle_command)
        llm_thread.start()
        
        # Add the thread to the active threads list
        window.active_threads.append(llm_thread)
    
    @staticmethod
    def handle_llm_response(window, response):
        """Handle a response from the LLM"""
        # Add the response to the chat window
        window.chat_window.add_message("Assistant", response)
        
        # Add to memory
        window.memory_manager.add_message("assistant", response)
    
    @staticmethod
    def handle_command(window, command):
        """Handle a command from the LLM"""
        # Execute the command
        window.execute_command(command)
