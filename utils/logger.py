from rich.console import Console
from rich.traceback import install
from rich.logging import RichHandler
import logging
import inspect
import os

install(show_locals=True)

console = Console()

def setup_logging():
    """Configure logging settings for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]",
        datefmt="%H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True, show_time=False)]
    )
    
    logger = logging.getLogger("interview_app")
    
    return logger

logger = setup_logger()

def log_info(message: str) -> None:
    """Log information message."""
    frame = inspect.currentframe().f_back
    file_path = os.path.relpath(frame.f_code.co_filename)
    logging.info(f"[INFO] {message} [Called from {file_path}:{frame.f_lineno}]")

def log_debug(message: str) -> None:
    """Log debug message."""
    frame = inspect.currentframe().f_back
    file_path = os.path.relpath(frame.f_code.co_filename)
    logging.debug(f"[DEBUG] {message} [Called from {file_path}:{frame.f_lineno}]")

def log_error(message: str, error: Exception) -> None:
    """Log error message with exception details."""
    frame = inspect.currentframe().f_back
    file_path = os.path.relpath(frame.f_code.co_filename)
    logging.error(f"[ERROR] {message} [Called from {file_path}:{frame.f_lineno}]: {str(error)}", exc_info=True)

def log_warning(message: str):
    frame = inspect.currentframe().f_back
    file_path = os.path.relpath(frame.f_code.co_filename)
    logger.warning(f"[WARNING] {message} [Called from {file_path}:{frame.f_lineno}]")

def log_success(message: str):
    frame = inspect.currentframe().f_back
    file_path = os.path.relpath(frame.f_code.co_filename)
    logger.info(f"[SUCCESS] ✓ {message} [Called from {file_path}:{frame.f_lineno}]")
