import logging

from bot.client import BinanceFuturesClient

from bot.models import (
    OrderRequest,
    OrderResponse,
)

from bot.exceptions import (
    BinanceClientError,
)


# =========================================================
# Logger
# =========================================================

logger = logging.getLogger(__name__)


# =========================================================
# Order Orchestration Service
# =========================================================

def place_order(
    order_request: OrderRequest,
    client: BinanceFuturesClient,
) -> OrderResponse:
    """
    Orchestrate order placement workflow.
    """

    # =====================================================
    # Workflow Start
    # =====================================================

    logger.info(
        "Placing %s %s order for %s.",
        order_request.order_type,
        order_request.side,
        order_request.symbol,
    )

    logger.debug(
        "Incoming OrderRequest: %s",
        order_request,
    )

    try:
        # =================================================
        # Submit Order
        # =================================================

        response = client.create_order(
            order_request
        )

        # =================================================
        # Success Logging
        # =================================================

        logger.info(
            "Order placed successfully. "
            "order_id=%s status=%s",
            response.order_id,
            response.status,
        )

        logger.debug(
            "Normalized OrderResponse: %s",
            response,
        )

        return response

    # =====================================================
    # Expected Client Failures
    # =====================================================

    except BinanceClientError as error:
        logger.error(
            "Order placement failed: %s",
            error,
        )

        raise

    # =====================================================
    # Unexpected Failures
    # =====================================================

    except Exception:
        logger.exception(
            "Unexpected order orchestration failure."
        )

        raise