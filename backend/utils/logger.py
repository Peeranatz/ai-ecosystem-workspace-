import logging
import os
import sys
import time
import traceback
from functools import wraps

# Ensure logs directory exists
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_DIR, "app.log")

def get_custom_logger(name: str = "AIEcosystem", log_level: str = "DEBUG") -> logging.Logger:
    """
    Creates and configures a custom Logger instance.
    Supports DEBUG, INFO, WARNING, ERROR, CRITICAL levels with both Console and File handlers.
    """
    logger = logging.getLogger(name)
    
    # Set numeric log level
    numeric_level = getattr(logging, log_level.upper(), logging.DEBUG)
    logger.setLevel(numeric_level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Detailed Log Format
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Console Handler (Standard Output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. File Handler (Appends to logs/app.log)
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Global default logger instance
logger = get_custom_logger()

def log_success(operation_name: str, duration_ms: float, details: dict = None):
    """
    Explicitly records a SUCCESS state with operational context and execution duration.
    """
    msg = f"[STATUS: SUCCESS] Operation '{operation_name}' completed in {duration_ms:.2f}ms."
    if details:
        msg += f" Details: {details}"
    logger.info(msg)

def log_fail(operation_name: str, error: Exception, context: dict = None):
    """
    Explicitly records a FAIL state with error type, message, context parameters, and stack traceback.
    """
    error_type = type(error).__name__
    tb_str = traceback.format_exc().strip()
    msg = f"[STATUS: FAIL] Operation '{operation_name}' failed with {error_type}: {str(error)}"
    if context:
        msg += f" | Context: {context}"
    msg += f"\nTraceback:\n{tb_str}"
    logger.error(msg)

def log_execution(operation_name: str = None):
    """
    Decorator that automatically measures execution time and logs SUCCESS or FAIL states.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                log_success(op_name, duration_ms, details={"args": args, "kwargs": kwargs})
                return result
            except Exception as e:
                log_fail(op_name, e, context={"args": args, "kwargs": kwargs})
                raise e
        return wrapper
    return decorator
