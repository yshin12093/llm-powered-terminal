#!/usr/bin/env python3
from terminal_executor import TerminalExecutor
from llm_thread import LLMThread

class CommandHandlers:
    """
    Handlers for terminal command execution and error analysis
    """
    
    @staticmethod
    def setup_handlers(window):
        """
        Set up the command-related handlers for the main window
        
        Args:
            window: The MainWindow instance
        """
        window.execute_command = lambda command: CommandHandlers.execute_command(window, command)
        window.handle_command_output = lambda command, output, exit_code: CommandHandlers.handle_command_output(window, command, output, exit_code)
        window.analyze_error = lambda command, output, exit_code: CommandHandlers.analyze_error(window, command, output, exit_code)
    
    @staticmethod
    def execute_command(window, command):
        # Execute the command directly using TerminalExecutor
        window.terminal_executor = TerminalExecutor(command)
        window.terminal_executor.command_output.connect(
            lambda output, exit_code: window.handle_command_output(command, output, exit_code)
        )
        window.terminal_executor.finished.connect(
            lambda: window.active_threads.remove(window.terminal_executor) if window.terminal_executor in window.active_threads else None
        )
        
        # Add to active threads
        window.active_threads.append(window.terminal_executor)
        
        # Start the thread
        window.terminal_executor.start()
        
        # Notify in chat
        window.chat_window.add_message("Assistant", f"Executing: `{command}`")
    
    @staticmethod
    def handle_command_output(window, command, output, exit_code):
        # Check if terminal_output exists
        if not hasattr(window, 'terminal_output'):
            print("ERROR: window.terminal_output does not exist!")
            return
            
        # Display in terminal output
        try:
            window.terminal_output.add_output(command, output, exit_code)
        except Exception as e:
            print(f"ERROR in terminal_output.add_output: {str(e)}")
        
        # Add to memory
        window.memory_manager.add_command_result(command, output, exit_code)
        
        # If command failed, send to LLM for analysis
        if exit_code != 0:
            window.analyze_error(command, output, exit_code)
    
    @staticmethod
    def analyze_error(window, command, output, exit_code):
        error_message = (
            f"The command `{command}` failed with exit code {exit_code}. "
            f"Here's the output:\n\n```\n{output}\n```\n\n"
            f"What went wrong and how can I fix it?"
        )
        
        # Display user message (system generated)
        window.chat_window.add_message("System", "Analyzing command failure...")
        
        # Process with LLM
        llm_thread = LLMThread(
            error_message,
            window.memory_manager.get_messages()
        )
        llm_thread.response_ready.connect(window.handle_llm_response)
        llm_thread.command_ready.connect(window.execute_command)
        llm_thread.start()
        
        # Add to active threads
        window.active_threads.append(llm_thread)
