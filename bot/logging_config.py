import logging

from pathlib import Path
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler


# =========================================================
# Logging Constants
# =========================================================

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(name)s:%(lineno)d | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

MAX_LOG_SIZE = 5 * 1024 * 1024
BACKUP_COUNT = 3


# =========================================================
# Logging Setup
# =========================================================


def setup_logging(
    verbose: bool = False,
) -> logging.Logger:
    """
    Configure application logging.
    """

    logger = logging.getLogger("trading_bot")

    # =====================================================
    # Prevent Duplicate Handlers
    # =====================================================

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    logger.propagate = False

    # =====================================================
    # Create Logs Directory
    # =====================================================

    Path("logs").mkdir(exist_ok=True)

    # =====================================================
    # File Handler
    # =====================================================

    file_handler = RotatingFileHandler(
        filename="logs/trading_bot.log",
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    file_handler.setFormatter(file_formatter)

    # =====================================================
    # Console Handler
    # =====================================================

    console_handler = RichHandler(
        rich_tracebacks=True,
        show_path=True,
        markup=True,
    )

    console_handler.setLevel(
        logging.DEBUG if verbose else logging.WARNING
    )

    console_formatter = logging.Formatter(
        fmt="%(message)s",
    )

    console_handler.setFormatter(
        console_formatter
    )

    # =====================================================
    # Attach Handlers
    # =====================================================

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger