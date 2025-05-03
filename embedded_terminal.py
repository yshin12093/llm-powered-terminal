#!/usr/bin/env python3
import os
import signal
import subprocess
import pty
import select
import fcntl
import termios
import struct
import re
from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QTextCursor, QKeyEvent

class EmbeddedTerminal(QTextEdit):
    """A terminal emulator widget that runs a real shell"""
    
    command_executed = Signal(str, str, int)  # command, output, exit_code
    
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Menlo", 20))
        self.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0;")
        self.setReadOnly(False)
        
        # Terminal process
        self.process = None
        self.master_fd = None
        self.slave_fd = None
        
        # Command history
        self.command_history = []
        self.history_index = 0
        
        # Current command being typed
        self.current_command = ""
        self.prompt = ""
        self.prompt_length = 0
        
        # Start the terminal
        self.start_terminal()
        
        # Set up a timer to read output
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_output)
        self.timer.start(100)  # Read every 100ms
    
    def start_terminal(self):
        """Start a new terminal process"""
        # Create a pseudo-terminal
        self.master_fd, self.slave_fd = pty.openpty()
        
        # Make the master non-blocking
        flags = fcntl.fcntl(self.master_fd, fcntl.F_GETFL)
        fcntl.fcntl(self.master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        
        # Set terminal size
        rows, cols = 24, 80
        term_size = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(self.slave_fd, termios.TIOCSWINSZ, term_size)
        
        # Start shell process
        env = os.environ.copy()
        env["TERM"] = "xterm-256color"
        
        self.process = subprocess.Popen(
            ["/bin/zsh"],
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            universal_newlines=True,
            env=env,
            preexec_fn=os.setsid,
            close_fds=True
        )
        
        # Close the slave file descriptor as the child process has it
        os.close(self.slave_fd)
        
        # Read initial prompt
        self.read_output()
    
    def read_output(self):
        """Read output from the terminal process"""
        if self.process is None or self.master_fd is None:
            return
            
        # Check if there's data to read
        r, w, e = select.select([self.master_fd], [], [], 0)
        if not r:
            return
            
        try:
            data = os.read(self.master_fd, 1024).decode('utf-8', errors='replace')
            if data:
                # Clean ANSI escape sequences
                clean_data = self.clean_ansi(data)
                
                # Store the cursor position
                cursor = self.textCursor()
                cursor_pos = cursor.position()
                
                # Insert the clean data
                cursor.movePosition(QTextCursor.End)
                cursor.insertText(clean_data)
                
                # Update the prompt if needed
                if '\n' in clean_data or '\r' in clean_data:
                    self.update_prompt()
                
                # Move cursor to end
                cursor.movePosition(QTextCursor.End)
                self.setTextCursor(cursor)
                
                # Scroll to the bottom
                self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        except (OSError, IOError) as e:
            if e.errno != 11:  # EAGAIN (Resource temporarily unavailable)
                print(f"Error reading from terminal: {e}")
                
    def clean_ansi(self, text):
        """Remove ANSI escape sequences from text"""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def update_prompt(self):
        """Update the current prompt"""
        text = self.toPlainText()
        lines = text.split('\n')
        if lines:
            self.prompt = lines[-1]
            self.prompt_length = len(self.prompt)
            self.current_command = ""
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if self.process is None or self.process.poll() is not None:
            return
            
        key = event.key()
        
        # Handle special keys
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            # Execute command
            command = self.current_command.strip()
            if command:
                self.command_history.append(command)
                self.history_index = len(self.command_history)
                
                # Send command to process
                os.write(self.master_fd, (command + '\n').encode())
                
                # Reset current command
                self.current_command = ""
            else:
                # Just send a newline
                os.write(self.master_fd, '\n'.encode())
                
        elif key == Qt.Key_Backspace:
            # Delete character if not at prompt
            if self.current_command:
                self.current_command = self.current_command[:-1]
                super().keyPressEvent(event)
                
        elif key == Qt.Key_Up:
            # Previous command in history
            if self.command_history and self.history_index > 0:
                self.history_index -= 1
                
                # Remove current command
                cursor = self.textCursor()
                for _ in range(len(self.current_command)):
                    cursor.deletePreviousChar()
                
                # Insert command from history
                self.current_command = self.command_history[self.history_index]
                cursor.insertText(self.current_command)
                
        elif key == Qt.Key_Down:
            # Next command in history
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                
                # Remove current command
                cursor = self.textCursor()
                for _ in range(len(self.current_command)):
                    cursor.deletePreviousChar()
                
                # Insert command from history
                self.current_command = self.command_history[self.history_index]
                cursor.insertText(self.current_command)
            elif self.history_index == len(self.command_history) - 1:
                # At the end of history, clear command
                self.history_index = len(self.command_history)
                
                # Remove current command
                cursor = self.textCursor()
                for _ in range(len(self.current_command)):
                    cursor.deletePreviousChar()
                
                self.current_command = ""
                
        elif key == Qt.Key_Tab:
            # Send tab for completion
            os.write(self.master_fd, '\t'.encode())
            
        elif key == Qt.Key_C and event.modifiers() & Qt.ControlModifier:
            # Ctrl+C - send SIGINT
            if self.process:
                os.kill(self.process.pid, signal.SIGINT)
                
        elif key == Qt.Key_D and event.modifiers() & Qt.ControlModifier:
            # Ctrl+D - send EOF
            if self.process:
                os.write(self.master_fd, '\x04'.encode())
                
        else:
            # Regular character
            text = event.text()
            if text:
                self.current_command += text
                super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Clean up when the widget is closed"""
        if self.process:
            try:
                os.kill(self.process.pid, signal.SIGTERM)
            except OSError:
                pass
            
            self.process = None
            
        if self.master_fd:
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            
            self.master_fd = None
            
        if self.timer.isActive():
            self.timer.stop()
            
        super().closeEvent(event)
