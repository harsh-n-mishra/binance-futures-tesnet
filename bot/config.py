import os

from dataclasses import dataclass
from dotenv import load_dotenv

from bot.validators import (
    validate_api_key,
    validate_api_secret,
    validate_environment,
    validate_request_timeout,
    validate_log_path,
)


# Load environment variables from .env
load_dotenv()


BASE_URLS = {
    "testnet": "https://testnet.binancefuture.com",
    "mainnet": "https://fapi.binance.com",
}


@dataclass(frozen=True)
class Settings:
    api_key: str
    api_secret: str
    environment: str
    base_url: str
    request_timeout: float
    log_path: str


def load_settings() -> Settings:
    """
    Load and validate application settings.
    """

    # =========================
    # Raw Environment Variables
    # =========================

    raw_api_key = os.getenv("BINANCE_API_KEY")
    raw_api_secret = os.getenv("BINANCE_API_SECRET")
    raw_environment = os.getenv("BINANCE_ENV", "testnet")
    raw_timeout = os.getenv("REQUEST_TIMEOUT", "10")
    raw_log_path = os.getenv(
        "LOG_PATH",
        "logs/trading_bot.log"
    )

    # =========================
    # Validation + Normalization
    # =========================

    api_key = validate_api_key(raw_api_key)
    api_secret = validate_api_secret(raw_api_secret)

    environment = validate_environment(raw_environment)

    request_timeout = validate_request_timeout(raw_timeout)

    log_path = validate_log_path(raw_log_path)

    # =========================
    # Resolve Base URL
    # =========================

    base_url = BASE_URLS[environment]

    # =========================
    # Build Settings Object
    # =========================

    return Settings(
        api_key=api_key,
        api_secret=api_secret,
        environment=environment,
        base_url=base_url,
        request_timeout=request_timeout,
        log_path=log_path,
    )


# Global immutable settings object
settings = load_settings()