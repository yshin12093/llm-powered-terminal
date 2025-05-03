#!/usr/bin/env python3
"""
Command parser for converting natural language to terminal commands using LLM
"""
import ollama
from llm_prompts import COMMAND_PARSER_PROMPT

def parse_direct_command(message):
    """
    Use LLM to parse natural language into terminal commands
    
    Args:
        message: The user message
        
    Returns:
        A command string if a command can be derived, None otherwise
    """
    # Quick check for empty messages
    if not message or not message.strip():
        return None
        
    # Check if the message is already a common terminal command
    # This is a simple optimization to avoid LLM calls for obvious commands
    first_word = message.strip().split()[0].lower()
    common_commands = ['ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'grep', 'find', 'pwd']
    if first_word in common_commands:
        return message.strip()
    
    try:
        # Prepare the prompt for command parsing
        system_message = {
            "role": "system",
            "content": COMMAND_PARSER_PROMPT
        }
        
        # Add the user message
        user_message = {
            "role": "user",
            "content": message
        }
        
        # Generate response using Ollama with Llama 3
        response = ollama.chat(
            model="llama3",
            messages=[system_message, user_message],
            options={"temperature": 0.0}  # Low temperature for more deterministic responses
        )
        
        # Extract the assistant's message
        assistant_message = response["message"]["content"]
        
        # If the response is "NONE", return None
        if assistant_message.strip().upper() == "NONE":
            return None
            
        # Otherwise, return the command
        return assistant_message.strip()
        
    except Exception as e:
        print(f"Error using LLM for command parsing: {str(e)}")
        # Fall back to simple parsing for common phrases
        if message.lower().startswith("cd ") or message.lower().startswith("go to "):
            # Extract directory name
            if message.lower().startswith("cd "):
                dir_name = message[3:].strip()
            else:  # go to
                dir_name = message[5:].strip()
            return f"cd {dir_name}"
        
        return None
