import tkinter as tk
from tkinter import ttk
from core.log.logger import logger, log_queue

class LogViewer(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Text widget for logs
        self.log_text = tk.Text(self, height=20, wrap="word", state="disabled", bg="black", fg="white")
        self.log_text.pack(expand=True, fill="both", padx=5, pady=5)
        self.log_text.insert(tk.END, "[INFO] System initialized...\n")

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.log_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=self.scrollbar.set)
        
        # Buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill="x", pady=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear Logs", command=self.clear_logs)
        self.clear_button.pack(side="right", padx=5)

        # Start updating logs
        self.update_logs()

    def update_logs(self):
        """Fetch logs from the queue and display them in the Text widget."""
        while not log_queue.empty():
            log_message = log_queue.get_nowait()
            self.append_log(log_message)
        self.after(100, self.update_logs)  # Schedule next update

    def append_log(self, message):
        """Append a log message to the Text widget."""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.yview(tk.END)  # Auto-scroll

    def clear_logs(self):
        """Clear the logs from the Text widget."""
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")