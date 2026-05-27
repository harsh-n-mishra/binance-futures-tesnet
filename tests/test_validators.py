import pytest

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
    ValidationError,
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

    except ValidationError:
        assert True

    else:
        assert False


def test_validate_stop_order_success():
    order_request = validate_order_request(
        symbol="btcusdt",
        side="buy",
        order_type="stop",
        quantity="0.01",
        price="65000",
        stop_price="64900",
    )

    assert order_request.order_type == "STOP"
    assert order_request.price == Decimal("65000")
    assert order_request.stop_price == Decimal("64900")


def test_stop_order_requires_stop_price():
    with pytest.raises(ValidationError):
        validate_order_request(
            symbol="BTCUSDT",
            side="BUY",
            order_type="STOP",
            quantity="0.01",
            price="65000",
        )


def test_market_order_cannot_have_price():
    with pytest.raises(ValidationError):
        validate_order_request(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.01",
            price="65000",
        )


def test_market_order_cannot_have_stop_price():
    with pytest.raises(ValidationError):
        validate_order_request(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.01",
            stop_price="64000",
        )


def test_limit_order_cannot_have_stop_price():
    with pytest.raises(ValidationError):
        validate_order_request(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity="0.01",
            price="65000",
            stop_price="64000",
        )


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

    assert request.stop_price is None