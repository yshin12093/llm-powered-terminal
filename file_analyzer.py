#!/usr/bin/env python3
import os
import ollama
from pathlib import Path
from PySide6.QtCore import QObject, Signal, Slot, QThread

class FileAnalyzer(QObject):
    """
    A utility class for analyzing files using Ollama with Llama 3
    """
    analysis_complete = Signal(str, str)  # file_path, analysis
    
    def __init__(self):
        super().__init__()
        
    def analyze_file(self, file_path):
        """
        Analyze a file using Ollama with Llama 3
        
        Args:
            file_path (str or Path): Path to the file to analyze
        """
        self.analyzer_thread = FileAnalyzerThread(file_path)
        self.analyzer_thread.analysis_ready.connect(
            lambda file_path, analysis: self.analysis_complete.emit(file_path, analysis)
        )
        self.analyzer_thread.start()


class FileAnalyzerThread(QThread):
    """Thread for file analysis using Ollama"""
    analysis_ready = Signal(str, str)  # file_path, analysis
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = Path(file_path)
        
    def run(self):
        try:
            # Read file content
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate prompt for the model
            prompt = f"Please analyze the following file and provide a concise summary:\n\nFilename: {self.file_path.name}\nContent:\n{content}\n\nAnalysis summary (focus on main purpose, key components, and important details):"
            
            # Generate analysis with Ollama using Llama 3
            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            
            # Extract the analysis
            analysis = response["message"]["content"]
            
            self.analysis_ready.emit(str(self.file_path), analysis)
            
        except Exception as e:
            self.analysis_ready.emit(str(self.file_path), f"Error analyzing file: {str(e)}")
