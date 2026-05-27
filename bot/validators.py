import re

from decimal import Decimal, InvalidOperation
from typing import Optional, Union, Type

from bot.models import OrderRequest

from bot.exceptions import (
    ConfigurationError,
    InvalidEnvironmentError,
    InvalidOrderTypeError,
    InvalidPriceError,
    InvalidQuantityError,
    InvalidSideError,
    InvalidSymbolError,
    MissingEnvironmentVariableError,
    ValidationError,
)


# =========================================================
# Environment Validation Constants
# =========================================================

VALID_ENVIRONMENTS = {"testnet", "mainnet"}


# =========================================================
# Trading Validation Constants
# =========================================================

VALID_ORDER_SIDES = {"BUY", "SELL"}

VALID_ORDER_TYPES = {
    "MARKET",
    "LIMIT",
    "STOP",
}

SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]+$")


# =========================================================
# Environment Validators
# =========================================================

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


# =========================================================
# Internal Decimal Helper
# =========================================================

def _validate_positive_decimal(
    value: Union[str, int, float, Decimal],
    field_name: str,
    exception_class: Type[Exception],
) -> Decimal:
    """
    Validate and normalize a positive Decimal value.
    """

    if value is None or str(value).strip() == "":
        raise exception_class(
            f"{field_name} is required."
        )

    try:
        normalized_value = Decimal(str(value).strip())

    except (InvalidOperation, ValueError) as error:
        raise exception_class(
            f"{field_name} must be a valid numeric value."
        ) from error

    if normalized_value <= 0:
        raise exception_class(
            f"{field_name} must be greater than zero."
        )

    return normalized_value


# =========================================================
# Field Validators
# =========================================================

def validate_symbol(symbol: str) -> str:
    """
    Validate and normalize trading symbol.
    """

    if not symbol or not symbol.strip():
        raise InvalidSymbolError(
            "Symbol cannot be empty."
        )

    normalized_symbol = symbol.strip().upper()

    if not SYMBOL_PATTERN.fullmatch(normalized_symbol):
        raise InvalidSymbolError(
            "Symbol must contain only letters and numbers."
        )

    return normalized_symbol


def validate_side(side: str) -> str:
    """
    Validate and normalize order side.
    """

    if not side or not side.strip():
        raise InvalidSideError(
            "Order side cannot be empty."
        )

    normalized_side = side.strip().upper()

    if normalized_side not in VALID_ORDER_SIDES:
        allowed = ", ".join(sorted(VALID_ORDER_SIDES))

        raise InvalidSideError(
            f"Invalid side. Allowed values: {allowed}."
        )

    return normalized_side


def validate_order_type(order_type: str) -> str:
    """
    Validate and normalize order type.
    """

    if not order_type or not order_type.strip():
        raise InvalidOrderTypeError(
            "Order type cannot be empty."
        )

    normalized_order_type = order_type.strip().upper()

    if normalized_order_type not in VALID_ORDER_TYPES:
        allowed = ", ".join(sorted(VALID_ORDER_TYPES))

        raise InvalidOrderTypeError(
            f"Invalid order type. "
            f"Allowed values: {allowed}."
        )

    return normalized_order_type


def validate_quantity(
    quantity: Union[str, int, float, Decimal],
) -> Decimal:
    """
    Validate and normalize order quantity.
    """

    return _validate_positive_decimal(
        value=quantity,
        field_name="Quantity",
        exception_class=InvalidQuantityError,
    )


def validate_price(
    price: Optional[Union[str, int, float, Decimal]],
) -> Optional[Decimal]:
    """
    Validate and normalize order price.
    """

    if price is None or str(price).strip() == "":
        return None

    return _validate_positive_decimal(
        value=price,
        field_name="Price",
        exception_class=InvalidPriceError,
    )


def validate_stop_price(
    stop_price: str | int | float | Decimal | None,
) -> Decimal | None:
    """
    Validate stop price.
    """

    if stop_price is None:
        return None

    if isinstance(stop_price, str):
        stop_price = stop_price.strip()

        if stop_price == "":
            return None

    try:
        normalized_stop_price = Decimal(str(stop_price))
    except (InvalidOperation, ValueError) as error:
        raise InvalidPriceError(
            "Stop price must be a valid numeric value."
        ) from error

    if normalized_stop_price <= 0:
        raise InvalidPriceError(
            "Stop price must be greater than zero."
        )

    return normalized_stop_price


# =========================================================
# Master Validator
# =========================================================

def validate_order_request(
    symbol: str,
    side: str,
    order_type: str,
    quantity: Union[str, int, float, Decimal],
    price: Optional[Union[str, int, float, Decimal]] = None,
    stop_price: Optional[
        Union[str, int, float, Decimal]
    ] = None,
) -> OrderRequest:
    """
    Validate, normalize, and construct
    a trusted OrderRequest model.
    """

    # =========================
    # Field Validation
    # =========================

    validated_symbol = validate_symbol(symbol)

    validated_side = validate_side(side)

    validated_order_type = validate_order_type(
        order_type
    )

    validated_quantity = validate_quantity(
        quantity
    )

    validated_price = validate_price(price)

    validated_stop_price = validate_stop_price(
        stop_price
    )

    # =========================================================
    # Cross-Field Validation
    # =========================================================

    if validated_order_type == "MARKET":

        if validated_price is not None:
            raise ValidationError(
                "MARKET orders cannot specify price."
            )

        if validated_stop_price is not None:
            raise ValidationError(
                "MARKET orders cannot specify stop price."
            )

    elif validated_order_type == "LIMIT":

        if validated_price is None:
            raise ValidationError(
                "LIMIT orders require a price."
            )

        if validated_stop_price is not None:
            raise ValidationError(
                "LIMIT orders cannot specify stop price."
            )

    elif validated_order_type == "STOP":

        if validated_price is None:
            raise ValidationError(
                "STOP orders require a price."
            )

        if validated_stop_price is None:
            raise ValidationError(
                "STOP orders require a stop price."
            )

    # =========================
    # Construct Trusted Model
    # =========================

    return OrderRequest(
        symbol=validated_symbol,
        side=validated_side,
        order_type=validated_order_type,
        quantity=validated_quantity,
        price=validated_price,
        stop_price=validated_stop_price,
    )