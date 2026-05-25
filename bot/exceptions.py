# feat: implement domain-based exception architecture

class TradingBotError(Exception):
    """Base exception for all trading bot errors."""


# =========================================================
# Configuration Exceptions
# =========================================================

class ConfigurationError(TradingBotError):
    """Base exception for configuration-related errors."""


class MissingEnvironmentVariableError(ConfigurationError):
    """Raised when a required environment variable is missing."""


class InvalidEnvironmentError(ConfigurationError):
    """Raised when an invalid environment configuration is provided."""


# =========================================================
# Validation Exceptions
# =========================================================

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


# =========================================================
# Binance Client Exceptions
# =========================================================

class BinanceClientError(TradingBotError):
    """Base exception for Binance client-related errors."""


class AuthenticationError(BinanceClientError):
    """Raised when Binance authentication fails."""


class NetworkError(BinanceClientError):
    """Raised when a network-related error occurs."""


class RequestTimeoutError(NetworkError):
    """Raised when a Binance request times out."""


class APIResponseError(BinanceClientError):
    """Raised when Binance returns an invalid or failed API response."""


class OrderPlacementError(BinanceClientError):
    """Raised when order placement fails."""