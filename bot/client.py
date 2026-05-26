import logging

from decimal import Decimal
from typing import Any, Dict

from requests.exceptions import (
    ConnectionError,
    Timeout,
)

from binance.client import Client
from binance.exceptions import (
    BinanceAPIException,
    BinanceRequestException,
)

from bot.config import Settings
from bot.models import (
    OrderRequest,
    OrderResponse,
)

from bot.exceptions import (
    APIResponseError,
    AuthenticationError,
    NetworkError,
    OrderPlacementError,
    RequestTimeoutError,
)


# =========================================================
# Logger
# =========================================================

logger = logging.getLogger(__name__)


# =========================================================
# Binance Futures Client
# =========================================================

class BinanceFuturesClient:
    """
    Binance USDT-M Futures client abstraction.
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize Binance SDK client.
        """

        self.settings = settings

        logger.debug(
            "Initializing Binance Futures client."
        )

        self.client = Client(
            api_key=settings.api_key,
            api_secret=settings.api_secret,
            requests_params={
                "timeout": settings.request_timeout,
            },
        )

        # =================================================
        # Configure Futures Base URL
        # =================================================

        self.client.FUTURES_URL = (
            # settings.base_url
            f"{settings.base_url}/fapi"
        )

        logger.info(
            "Binance Futures client initialized."
        )

    # =====================================================
    # Connectivity Check
    # =====================================================

    def ping(self) -> None:
        """
        Verify Binance connectivity.
        """

        logger.debug(
            "Pinging Binance Futures API."
        )

        try:
            self.client.ping()

            logger.info(
                "Binance API ping successful."
            )

        except Timeout as error:
            logger.error(
                "Binance API ping timed out."
            )

            raise RequestTimeoutError(
                "Connection timeout while "
                "reaching Binance API."
            ) from error

        except ConnectionError as error:
            logger.error(
                "Unable to connect to Binance API."
            )

            raise NetworkError(
                "Unable to connect to Binance API."
            ) from error

        except BinanceRequestException as error:
            logger.error(
                "Binance request error during ping: %s",
                error,
            )

            raise NetworkError(
                "Binance network request failed."
            ) from error

        except Exception as error:
            logger.exception(
                "Unexpected error during ping."
            )

            raise APIResponseError(
                "Unexpected Binance API error."
            ) from error

    # =====================================================
    # Authentication Check
    # =====================================================

    def test_authentication(self) -> None:
        """
        Verify Binance API authentication.
        """

        logger.debug(
            "Testing Binance API authentication."
        )

        try:
            self.client.futures_account_balance()

            logger.info(
                "Binance authentication successful."
            )

        except BinanceAPIException as error:
            logger.error(
                "Binance authentication failed: %s",
                error,
            )

            raise AuthenticationError(
                "Binance authentication failed."
            ) from error

        except Timeout as error:
            logger.error(
                "Authentication request timed out."
            )

            raise RequestTimeoutError(
                "Authentication request timed out."
            ) from error

        except ConnectionError as error:
            logger.error(
                "Network error during authentication."
            )

            raise NetworkError(
                "Unable to connect to Binance API."
            ) from error

        except Exception as error:
            logger.exception(
                "Unexpected authentication error."
            )

            raise APIResponseError(
                "Unexpected Binance authentication error."
            ) from error

    # =====================================================
    # Payload Builder
    # =====================================================

    def _build_payload(
        self,
        order_request: OrderRequest,
    ) -> Dict[str, Any]:
        """
        Build Binance Futures order payload.
        """

        payload = {
            "symbol": order_request.symbol,
            "side": order_request.side,
            "type": order_request.order_type,
            "quantity": str(
                order_request.quantity
            ),
        }

        # ================================================
        # LIMIT Order Fields
        # ================================================

        if order_request.order_type == "LIMIT":
            payload["price"] = str(
                order_request.price
            )

            payload["timeInForce"] = "GTC"

        logger.debug(
            "Built Binance payload: %s",
            payload,
        )

        return payload

    # =====================================================
    # Response Normalization
    # =====================================================

    def _normalize_response(
        self,
        response: Dict[str, Any],
    ) -> OrderResponse:
        """
        Normalize Binance order response.
        """

        avg_price = response.get(
            "avgPrice"
        )

        normalized_avg_price = (
            Decimal(avg_price)
            if avg_price
            and Decimal(avg_price) > 0
            else None
        )

        normalized_response = OrderResponse(
            order_id=str(
                response["orderId"]
            ),
            status=response["status"],
            executed_qty=Decimal(
                response["executedQty"]
            ),
            avg_price=normalized_avg_price,
            symbol=response["symbol"],
            side=response["side"],
            order_type=response["type"],
        )

        logger.debug(
            "Normalized Binance response: %s",
            normalized_response,
        )

        return normalized_response

    # =====================================================
    # Order Submission
    # =====================================================

    def create_order(
        self,
        order_request: OrderRequest,
    ) -> OrderResponse:
        """
        Submit Binance Futures order.
        """

        payload = self._build_payload(
            order_request
        )

        logger.debug(
            "Submitting Binance Futures order."
        )

        try:
            response = (
                self.client.futures_create_order(
                    **payload
                )
            )

            logger.info(
                "Binance order submitted successfully."
            )

            logger.info(
                "Raw Binance response: %s",
                response,
            )

            return self._normalize_response(
                response
            )

        # ================================================
        # Binance API Errors
        # ================================================

        except BinanceAPIException as error:
            logger.error(
                "Binance API order error: %s",
                error,
            )

            error_message = (
                error.message
                if hasattr(error, "message")
                else str(error)
            )

            # ============================================
            # Authentication Failures
            # ============================================

            if (
                "API-key" in error_message
                or "signature" in error_message
                or error.status_code == 401
            ):
                raise AuthenticationError(
                    "Binance authentication failed."
                ) from error

            # ============================================
            # Order Rejections
            # ============================================

            raise OrderPlacementError(
                f"Order rejected by Binance: "
                f"{error_message}"
            ) from error

        # ================================================
        # Network / Request Errors
        # ================================================

        except Timeout as error:
            logger.error(
                "Order request timed out."
            )

            raise RequestTimeoutError(
                "Order request timed out."
            ) from error

        except ConnectionError as error:
            logger.error(
                "Network error during order submission."
            )

            raise NetworkError(
                "Unable to connect to Binance API."
            ) from error

        except BinanceRequestException as error:
            logger.error(
                "Binance request exception: %s",
                error,
            )

            raise NetworkError(
                "Binance request failed."
            ) from error

        # ================================================
        # Unexpected Failures
        # ================================================

        except Exception as error:
            logger.exception(
                "Unexpected order submission error."
            )

            raise APIResponseError(
                "Unexpected Binance API error."
            ) from error