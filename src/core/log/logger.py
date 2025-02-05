import logging
import os
import queue
import logging.handlers

# Ensure the logs directory exists
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Queue for logging (used for real-time GUI updates)
log_queue = queue.Queue()

class QueueHandler(logging.Handler):
    """Custom logging handler to send logs to a queue."""
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        log_entry = self.format(record)
        self.log_queue.put(log_entry)

def setup_logger():
    """Configure application logging."""
    logger = logging.getLogger("AlasLogger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # Clear previous handlers to prevent duplicates

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")

    # File Handler (Writes logs to a file)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        encoding="utf-8",
        maxBytes=20 * 1024 * 1024,  # 20 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Queue Handler (For Tkinter GUI)
    queue_handler = QueueHandler(log_queue)
    queue_handler.setFormatter(formatter)
    logger.addHandler(queue_handler)

    return logger

# Initialize logger
logger = setup_logger()

# Example usage:
# logger.info("Application started.")
# logger.warning("Something might be wrong.")
