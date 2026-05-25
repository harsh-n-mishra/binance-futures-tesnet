class TradingBotError(Exception):
    """Base exception for the trading bot."""


# =========================
# Configuration Exceptions
# =========================

class ConfigurationError(TradingBotError):
    """Base exception for configuration-related errors."""


class MissingEnvironmentVariableError(ConfigurationError):
    """Raised when a required environment variable is missing."""


class InvalidEnvironmentError(ConfigurationError):
    """Raised when an invalid environment is provided."""


# =========================
# Validation Exceptions
# =========================

class ValidationError(TradingBotError):
    """Base exception for validation-related errors."""


class InvalidSymbolError(ValidationError):
    """Raised when a trading symbol is invalid."""


class InvalidSideError(ValidationError):
    """Raised when an order side is invalid."""


class InvalidOrderTypeError(ValidationError):
    """Raised when an order type is invalid."""


class InvalidQuantityError(ValidationError):
    """Raised when an order quantity is invalid."""


class InvalidPriceError(ValidationError):
    """Raised when an order price is invalid."""