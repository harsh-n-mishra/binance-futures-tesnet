# Binance Futures Trading Bot CLI

Python CLI trading client for Binance USDT-M Futures Testnet built with a layered backend architecture, validation-first workflow, structured exception handling, and professional operational logging.

---

# Overview

This project is a Python-based CLI trading bot that connects to the Binance USDT-M Futures Testnet and supports:

* MARKET orders
* LIMIT orders
* STOP (stop-limit) orders

The project focuses heavily on backend engineering quality rather than feature quantity.

Core engineering goals include:

* clean layered architecture
* immutable domain models
* validation-first request flow
* exchange abstraction
* structured exception handling
* operational observability
* professional CLI UX

The application validates and normalizes requests before any Binance API interaction occurs.

---

# Quick Start

## 1. Clone Repository

```bash
git clone <repository-url>
cd trading_bot
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Copy:

```bash
cp .env.example .env
```

Then populate:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
BINANCE_ENV=testnet
REQUEST_TIMEOUT=10
LOG_PATH=logs/trading_bot.log
```

---

## 5. Run Application

### MARKET Order

```bash
python run.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

---

# Features

## Trading Features

* Binance USDT-M Futures Testnet integration
* MARKET order support
* LIMIT order support
* STOP (stop-limit) order support
* Request normalization and validation
* Structured order response rendering

---

## Backend Engineering Features

* layered application architecture
* immutable dataclass-based domain models
* validation-first request pipeline
* exchange abstraction layer
* structured exception hierarchy
* exception translation from Binance SDK
* rotating file logging
* Rich-powered CLI rendering
* graceful runtime failure handling
* verbose operational diagnostics mode

---

# Architecture

## High-Level Flow

```text
CLI
  ↓
Validation Layer
  ↓
Orders Service
  ↓
Binance Client
  ↓
Binance Futures API
```

---

## Layer Responsibilities

| Layer               | Responsibility                                      |
| ------------------- | --------------------------------------------------- |
| `cli.py`            | CLI parsing, Rich rendering, exception presentation |
| `validators.py`     | normalization and validation                        |
| `orders.py`         | orchestration workflow                              |
| `client.py`         | Binance SDK abstraction and API communication       |
| `models.py`         | immutable request/response contracts                |
| `exceptions.py`     | domain exception hierarchy                          |
| `logging_config.py` | logging setup and observability                     |

---

# Project Structure

```text
trading_bot/
│
├── bot/
│   ├── client.py
│   ├── config.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── models.py
│   ├── orders.py
│   ├── validators.py
│   └── utils.py
│
├── logs/
│   └── trading_bot.log
│
├── tests/
│   └── test_validators.py
│
├── cli.py
├── run.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# Design Decisions

## Decimal Precision

`Decimal` is used instead of `float` for all financial values to avoid floating-point precision issues.

---

## Immutable Domain Models

Request and response models use:

```python
@dataclass(frozen=True, slots=True)
```

This creates:

* predictable state flow
* safer request handling
* reduced accidental mutation risk

---

## Validation-First Architecture

All user input is:

1. normalized
2. validated
3. converted into trusted immutable models

before any API interaction occurs.

---

## Exchange Abstraction

The application never exposes raw Binance SDK objects outside the client layer.

The `BinanceFuturesClient` encapsulates:

* payload construction
* SDK interaction
* exception translation
* response normalization

---

## Exception Translation

Raw Binance SDK exceptions are translated into domain-specific exceptions such as:

* `AuthenticationError`
* `NetworkError`
* `OrderPlacementError`

This keeps upper layers exchange-agnostic.

---

## Operational Logging

The application uses:

* Rich console logging
* rotating file logs
* structured logging semantics
* verbose debug mode

---

# Environment Configuration

## Supported Environments

| Environment | Base URL                            |
| ----------- | ----------------------------------- |
| `testnet`   | `https://testnet.binancefuture.com` |
| `mainnet`   | `https://fapi.binance.com`          |

---

## Required Variables

| Variable             | Description                |
| -------------------- | -------------------------- |
| `BINANCE_API_KEY`    | Binance API key            |
| `BINANCE_API_SECRET` | Binance API secret         |
| `BINANCE_ENV`        | `testnet` or `mainnet`     |
| `REQUEST_TIMEOUT`    | request timeout in seconds |
| `LOG_PATH`           | file logging location      |

---

# Usage Examples

## MARKET Order

```bash
python run.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

---

## LIMIT Order

```bash
python run.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.001 \
  --price 65000
```

---

## STOP (Stop-Limit) Order

```bash
python run.py \
  --symbol BTCUSDT \
  --side BUY \
  --type STOP \
  --quantity 0.001 \
  --price 65000 \
  --stop-price 64900
```

---

## Verbose Mode

```bash
python run.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001 \
  --verbose
```

Verbose mode enables:

* DEBUG console logs
* payload visibility
* detailed operational diagnostics

---

# Sample Output

## Successful MARKET Order

```text
Binance Futures Testnet Trading Bot

Order Summary
┏━━━━━━━━━━┳━━━━━━━━━┓
┃ Field    ┃ Value   ┃
┡━━━━━━━━━━╇━━━━━━━━━┩
│ Symbol   │ BTCUSDT │
│ Side     │ BUY     │
│ Type     │ MARKET  │
│ Quantity │ 0.001   │
│ Price    │ -       │
└──────────┴─────────┘

╭──────────────────── Success ────────────────────╮
│ ✓ Binance Futures order submitted successfully. │
╰─────────────────────────────────────────────────╯

Order Response
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field         ┃ Value       ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ Order ID      │ 13177507527 │
│ Status        │ NEW         │
│ Executed Qty  │ 0.0000      │
│ Average Price │ -           │
│ Symbol        │ BTCUSDT     │
│ Side          │ BUY         │
│ Type          │ MARKET      │
└───────────────┴─────────────┘
```

---

## Validation Failure Example

```text
Binance Futures Testnet Trading Bot

╭──────────────── Validation Error ────────────────╮
│ LIMIT orders require a price.                   │
╰──────────────────────────────────────────────────╯
```

---

## Exchange Rejection Example

```text
╭────────────── Order Placement Error ─────────────╮
│ Binance rejected order: Invalid symbol.         │
╰──────────────────────────────────────────────────╯
```

---

# Logging

## Console Logging

Default mode prioritizes:

* clean CLI UX
* Rich rendering
* concise operational feedback

Verbose mode enables detailed diagnostics.

---

## File Logging

Logs are written to:

```text
logs/trading_bot.log
```

The application uses:

* rotating file logs
* structured timestamps
* per-module loggers
* DEBUG-level persistence

---

## Log Format

```text
timestamp | level | module | message
```

Example:

```text
2026-05-22 21:45:32 | INFO | bot.orders:65 | Order placed successfully.
```

---

# Error Handling

The application differentiates between:

| Error Type              | Behavior                          |
| ----------------------- | --------------------------------- |
| Validation errors       | clean Rich validation panels      |
| Authentication failures | explicit auth error handling      |
| Network failures        | graceful operational failures     |
| Exchange rejections     | translated Binance error messages |
| Unexpected failures     | logged diagnostics + generic UX   |

The application avoids exposing raw stack traces for expected runtime failures.

---

# Testing

Validator coverage includes:

* symbol validation
* side validation
* order type validation
* quantity validation
* price validation
* stop price validation
* cross-field validation rules
* normalization behavior
* negative validation scenarios

Run tests:

```bash
pytest
```

---

# Assumptions & Limitations

* Binance Futures Testnet focused
* no websocket streaming
* no persistent storage
* no retry policies implemented
* no order lifecycle polling
* no order cancellation support
* no trading strategies
* no portfolio/risk management

The project is intended as a backend engineering and trading system architecture exercise.

---

# Future Improvements

Potential future enhancements:

* websocket market streaming
* order cancellation support
* retry policies
* order status polling
* persistent trade history
* additional order types

---

# Final Notes

This project prioritizes:

* backend engineering quality
* operational correctness
* clean architecture
* validation rigor
* observability
* maintainable abstractions

over feature quantity.