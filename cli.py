import sys
import logging
import argparse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from bot.models import OrderRequest
from bot.validators import validate_order_request

from bot.exceptions import (
    BinanceClientError,
    ConfigurationError,
    ValidationError,
)


# =========================================================
# Console + Logger
# =========================================================

console = Console()

logger = logging.getLogger(__name__)


# =========================================================
# CLI Argument Parsing
# =========================================================

def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """

    parser = argparse.ArgumentParser(
        prog="trading-bot",
        description=(
            "Binance USDT-M Futures Testnet Trading Bot"
        ),
        epilog=(
            "Example:\n"
            "python cli.py "
            "--symbol BTCUSDT "
            "--side BUY "
            "--type MARKET "
            "--quantity 0.01"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair (e.g. BTCUSDT)",
    )

    parser.add_argument(
        "--side",
        required=True,
        help="Order side: BUY or SELL",
    )

    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        help="Order type: MARKET or LIMIT",
    )

    parser.add_argument(
        "--quantity",
        required=True,
        help="Order quantity",
    )

    parser.add_argument(
        "--price",
        required=False,
        help="Limit price (required for LIMIT orders)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose debug logging",
    )

    return parser.parse_args()


# =========================================================
# Rich Rendering Helpers
# =========================================================

def display_banner() -> None:
    """
    Display CLI application banner.
    """

    banner = Text(
        "Binance Futures Testnet Trading Bot",
        style="bold cyan",
        justify="center",
    )

    console.print()
    console.print(banner)
    console.rule(style="cyan")


def display_order_summary(
    order_request: OrderRequest,
) -> None:
    """
    Display validated order summary.
    """

    table = Table(
        title="Order Summary",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row(
        "Symbol",
        order_request.symbol,
    )

    table.add_row(
        "Side",
        order_request.side,
    )

    table.add_row(
        "Type",
        order_request.order_type,
    )

    table.add_row(
        "Quantity",
        str(order_request.quantity),
    )

    table.add_row(
        "Price",
        (
            str(order_request.price)
            if order_request.price is not None
            else "-"
        ),
    )

    console.print()
    console.print(table)


def display_success_panel(message: str) -> None:
    """
    Display success message panel.
    """

    panel = Panel(
        f"[bold green]✓ {message}[/bold green]",
        title="Success",
        border_style="green",
    )

    console.print()
    console.print(panel)


def display_error_panel(
    title: str,
    message: str,
) -> None:
    """
    Display error message panel.
    """

    panel = Panel(
        f"[bold red]{message}[/bold red]",
        title=title,
        border_style="red",
    )

    console.print()
    console.print(panel)


# =========================================================
# Main CLI Flow
# =========================================================

def main() -> None:
    """
    CLI application entry point.
    """

    try:
        # =========================
        # Banner
        # =========================

        display_banner()

        # =========================
        # Parse CLI Arguments
        # =========================

        args = parse_arguments()

        logger.debug(
            "Parsed CLI arguments: %s",
            args,
        )

        # =========================
        # Validation + Model Creation
        # =========================

        order_request = validate_order_request(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        logger.info(
            "Order request validated successfully."
        )

        logger.debug(
            "Validated OrderRequest: %s",
            order_request,
        )

        # =========================
        # Rich Output
        # =========================

        display_order_summary(order_request)

        display_success_panel(
            "Order request validated successfully.\n"
            "Ready for Binance submission."
        )

        sys.exit(0)

    # =====================================================
    # Validation Errors
    # =====================================================

    except ValidationError as error:
        logger.warning(
            "Validation failed: %s",
            error,
        )

        display_error_panel(
            title="Validation Error",
            message=str(error),
        )

        sys.exit(1)

    # =====================================================
    # Configuration Errors
    # =====================================================

    except ConfigurationError as error:
        logger.error(
            "Configuration error: %s",
            error,
        )

        display_error_panel(
            title="Configuration Error",
            message=str(error),
        )

        sys.exit(1)

    # =====================================================
    # Binance/API Errors
    # =====================================================

    except BinanceClientError as error:
        logger.error(
            "Binance client error: %s",
            error,
        )

        display_error_panel(
            title="Binance API Error",
            message=str(error),
        )

        sys.exit(1)

    # =====================================================
    # Unexpected Internal Errors
    # =====================================================

    except Exception:
        logger.exception(
            "Unexpected internal application error."
        )

        display_error_panel(
            title="Internal Error",
            message=(
                "Unexpected internal error occurred.\n"
                "See logs for details."
            ),
        )

        sys.exit(2)


# =========================================================
# Script Entrypoint
# =========================================================

if __name__ == "__main__":
    main()