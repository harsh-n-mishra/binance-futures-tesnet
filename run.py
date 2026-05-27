import logging
import sys

from cli import main as cli_main

from bot.config import load_settings
from bot.exceptions import ConfigurationError
from bot.logging_config import setup_logging


# =========================================================
# Bootstrap Entry Point
# =========================================================


def main() -> None:
    """
    Application bootstrap entry point.
    """

    verbose = "--verbose" in sys.argv

    try:
        # =================================================
        # Setup Logging
        # =================================================

        setup_logging(verbose=verbose)

        logger = logging.getLogger("trading_bot.run")

        logger.info(
            "Application starting..."
        )

        # =================================================
        # Load Configuration
        # =================================================

        settings = load_settings()

        logger.info(
            "Configuration loaded successfully."
        )

        logger.info(
            "Environment: %s",
            settings.environment,
        )

        logger.info(
            "Base URL: %s",
            settings.base_url,
        )

        # =================================================
        # Launch CLI
        # =================================================

        cli_main(settings=settings)

    except ConfigurationError as error:
        logging.getLogger(
            "trading_bot.run"
        ).error(
            "Configuration error during startup: %s",
            error,
        )

        sys.exit(1)

    except Exception:
        logging.getLogger(
            "trading_bot.run"
        ).exception(
            "Unexpected application startup error."
        )

        sys.exit(2)


if __name__ == "__main__":
    main()