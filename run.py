import sys

from bot.config import load_settings
from bot.exceptions import ConfigurationError


def main() -> None:
    """
    Application entry point.
    """

    try:
        print("Starting Trading Bot...")

        settings = load_settings()

        print(f"Environment: {settings.environment}")
        print(f"Base URL: {settings.base_url}")

        print("Configuration loaded successfully.")

    except ConfigurationError as error:
        print(f"ERROR: {error}")

        sys.exit(1)


if __name__ == "__main__":
    main()