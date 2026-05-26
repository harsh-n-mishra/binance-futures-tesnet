from decimal import Decimal

from bot.validators import (
    validate_order_request,
    validate_side,
    validate_symbol,
    validate_quantity,
)

from bot.exceptions import (
    InvalidPriceError,
    InvalidQuantityError,
    InvalidSideError,
    InvalidSymbolError,
)


# =========================================================
# Symbol Validation Tests
# =========================================================

def test_symbol_normalization():
    result = validate_symbol("btcusdt")

    assert result == "BTCUSDT"


def test_invalid_symbol():
    try:
        validate_symbol("BTC/USDT")

    except InvalidSymbolError:
        assert True

    else:
        assert False


# =========================================================
# Side Validation Tests
# =========================================================

def test_side_normalization():
    result = validate_side("buy")

    assert result == "BUY"


def test_invalid_side():
    try:
        validate_side("LONG")

    except InvalidSideError:
        assert True

    else:
        assert False


# =========================================================
# Quantity Validation Tests
# =========================================================

def test_valid_quantity():
    result = validate_quantity("0.01")

    assert result == Decimal("0.01")


def test_scientific_notation_quantity():
    result = validate_quantity("1e-3")

    assert result == Decimal("1e-3")


def test_invalid_quantity_zero():
    try:
        validate_quantity("0")

    except InvalidQuantityError:
        assert True

    else:
        assert False


def test_invalid_quantity_negative():
    try:
        validate_quantity("-1")

    except InvalidQuantityError:
        assert True

    else:
        assert False


# =========================================================
# Cross-Field Validation Tests
# =========================================================

def test_limit_order_requires_price():
    try:
        validate_order_request(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity="0.01",
        )

    except InvalidPriceError:
        assert True

    else:
        assert False


def test_market_order_ignores_price():
    request = validate_order_request(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity="0.01",
        price="50000",
    )

    assert request.price is None


# =========================================================
# Model Contract Test
# =========================================================

def test_order_request_model_creation():
    request = validate_order_request(
        symbol="btcusdt",
        side="buy",
        order_type="market",
        quantity="0.01",
    )

    assert request.symbol == "BTCUSDT"

    assert request.side == "BUY"

    assert request.order_type == "MARKET"

    assert request.quantity == Decimal("0.01")

    assert request.price is None