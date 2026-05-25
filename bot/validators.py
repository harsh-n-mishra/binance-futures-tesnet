from bot.exceptions import (
    MissingEnvironmentVariableError,
    InvalidEnvironmentError,
    ConfigurationError,
)


VALID_ENVIRONMENTS = {"testnet", "mainnet"}


def validate_api_key(api_key: str) -> str:
    """
    Validate Binance API key.
    """
    if not api_key or not api_key.strip():
        raise MissingEnvironmentVariableError(
            "Missing BINANCE_API_KEY environment variable."
        )

    return api_key.strip()


def validate_api_secret(api_secret: str) -> str:
    """
    Validate Binance API secret.
    """
    if not api_secret or not api_secret.strip():
        raise MissingEnvironmentVariableError(
            "Missing BINANCE_API_SECRET environment variable."
        )

    return api_secret.strip()


def validate_environment(environment: str) -> str:
    """
    Validate Binance environment.
    """
    if not environment or not environment.strip():
        raise MissingEnvironmentVariableError(
            "Missing BINANCE_ENV environment variable."
        )

    normalized_environment = environment.strip().lower()

    if normalized_environment not in VALID_ENVIRONMENTS:
        allowed = ", ".join(VALID_ENVIRONMENTS)

        raise InvalidEnvironmentError(
            f"Invalid BINANCE_ENV '{environment}'. "
            f"Allowed values: {allowed}."
        )

    return normalized_environment


def validate_request_timeout(timeout: str) -> float:
    """
    Validate request timeout.
    """
    if timeout is None or str(timeout).strip() == "":
        raise MissingEnvironmentVariableError(
            "Missing REQUEST_TIMEOUT environment variable."
        )

    try:
        normalized_timeout = float(timeout)
    except ValueError as error:
        raise ConfigurationError(
            "REQUEST_TIMEOUT must be a numeric value."
        ) from error

    if normalized_timeout <= 0:
        raise ConfigurationError(
            "REQUEST_TIMEOUT must be greater than 0."
        )

    return normalized_timeout


def validate_log_path(log_path: str) -> str:
    """
    Validate log path.
    """
    if not log_path or not log_path.strip():
        raise MissingEnvironmentVariableError(
            "Missing LOG_PATH environment variable."
        )

    return log_path.strip()