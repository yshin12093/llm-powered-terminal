#!/usr/bin/env python3
import ollama

try:
    # Get the list of models
    models = ollama.list()
    
    # Print the structure
    print("Type of models:", type(models))
    print("Models:", models)
    
    # Try to access the models attribute
    if hasattr(models, "models"):
        print("Models has 'models' attribute")
        for model in models.models:
            print(f"Model: {model}")
    else:
        print("Models does not have 'models' attribute")
        print("Dir of models:", dir(models))
    
except Exception as e:
    print(f"Error connecting to Ollama: {str(e)}")
    print(f"Error type: {type(e)}")
