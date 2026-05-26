from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


# =========================================================
# Order Request Model
# =========================================================

@dataclass(frozen=True, slots=True)
class OrderRequest:
    """
    Represents a validated and normalized order request.
    """

    symbol: str
    side: str
    order_type: str
    quantity: Decimal
    price: Optional[Decimal] = None


# =========================================================
# Order Response Model
# =========================================================

@dataclass(frozen=True, slots=True)
class OrderResponse:
    """
    Represents a normalized Binance order response.
    """

    order_id: str
    status: str
    executed_qty: Decimal
    avg_price: Optional[Decimal]
    symbol: str
    side: str
    order_type: str