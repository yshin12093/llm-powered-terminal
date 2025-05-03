#!/usr/bin/env python3
import ollama
import json

try:
    # Get the list of models
    models = ollama.list()
    
    # Print the structure
    print("Type of models:", type(models))
    print("Structure of models:", json.dumps(models, indent=2))
    
    # Check if llama3 is available
    if isinstance(models, dict) and "models" in models:
        # If the structure is {"models": [...]}
        llama3_available = any(model.get("name") == "llama3" for model in models["models"])
    else:
        # If the structure is a list of models
        llama3_available = any("llama3" in (model.get("name", "") if isinstance(model, dict) else "") for model in models)
    
    print("llama3 available:", llama3_available)
    
except Exception as e:
    print(f"Error connecting to Ollama: {str(e)}")
    print(f"Error type: {type(e)}")
