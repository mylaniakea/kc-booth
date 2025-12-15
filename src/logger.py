"""
Centralized logging configuration for kc-booth.

Provides consistent logging across all modules with proper formatting
and log levels.
"""
import logging
import sys
from typing import Optional

# Default log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Name for the logger (usually __name__)
        level: Optional log level override
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        logger.addHandler(handler)
    
    # Set level
    logger.setLevel(level or logging.INFO)
    
    return logger


# Create default logger for startup messages
startup_logger = get_logger("kc-booth.startup")
