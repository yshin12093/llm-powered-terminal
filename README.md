# LLM-Powered Terminal

A PySide6 application that provides a conversational LLM assistant for executing terminal commands and handling errors. This app functions as a personalized AI shell with memory, powered by Ollama with Llama 3.

## Features

- Chat interface to interact with a local LLM assistant (Llama 3 via Ollama)
- Execute terminal commands through natural language
- Real-time terminal output display with proper formatting
- Directory tracking and navigation using natural language
- Get help when commands fail with automatic error analysis
- Build memory over time for recurring issues
- Analyze files using Llama 3 to provide summaries and insights

## Prerequisites

1. Install Ollama from [https://ollama.com/](https://ollama.com/)
2. Pull the Llama 3 model:
   ```
   ollama pull llama3
   ```
3. Make sure Ollama is running

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python main.py
   ```

## Usage

- Type natural language requests in the chat input
- The assistant will interpret your request and execute terminal commands
- If a command fails, the assistant will suggest fixes or apply known solutions
- The assistant builds memory over time to better assist with recurring issues
- Click "Analyze File" to select a file for the LLM to analyze and summarize
