"""
Logger module for Crypto Vibeness server
Handles logging to both console and file
"""
import os
import logging
from datetime import datetime


class CryptoLogger:
    """Logger class for server events"""

    def __init__(self, log_dir="./data/logs"):
        """Initialize logger with file and console output"""
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = os.path.join(log_dir, f"log_{timestamp}.txt")

        # Setup logging
        self.logger = logging.getLogger("CryptoVibeness")
        self.logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_format)

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        file_handler.setFormatter(file_format)

        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def log(self, event_type, username, details):
        """Log an event"""
        message = f"[{event_type}] {username}: {details}"
        self.logger.info(message)

    def info(self, message):
        """Log info message"""
        self.logger.info(message)

    def error(self, message):
        """Log error message"""
        self.logger.error(message)

    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
