import logging

from pathlib import Path
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler


LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(name)s:%(lineno)d | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> logging.Logger:
    """
    Configure application logging.

    Returns:
        logging.Logger: Configured root logger.
    """

    # =========================
    # Create Logs Directory
    # =========================

    logs_directory = Path("logs")
    logs_directory.mkdir(exist_ok=True)

    log_file_path = logs_directory / "trading_bot.log"

    # =========================
    # Root Logger
    # =========================

    root_logger = logging.getLogger()

    # Prevent duplicate handlers
    if root_logger.handlers:
        return root_logger

    root_logger.setLevel(logging.DEBUG)

    # =========================
    # Formatters
    # =========================

    file_formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    console_formatter = logging.Formatter(
        fmt="%(name)s:%(lineno)d | %(message)s"
    )

    # =========================
    # Console Handler
    # =========================

    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
    )

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # =========================
    # Rotating File Handler
    # =========================

    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # =========================
    # Attach Handlers
    # =========================

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    return root_logger