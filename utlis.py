Utility functions for the medical chatbot application.
"""
import logging

def setup_logger():
    """Set up the logger for the application."""
    logger = logging.getLogger('medical_chatbot')
    logger.setLevel(logging.INFO)
    
    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Add formatter to ch
    ch.setFormatter(formatter)
    
    # Add ch to logger
    logger.addHandler(ch)
    
    return logger

# Initialize logger
logger = setup_logger()

def log_error(message):
    """Log an error message."""
    logger.error(message)

def log_info(message):
    """Log an informational message."""
    logger.info(message)
