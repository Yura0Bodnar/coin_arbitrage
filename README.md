# Cryptocurrency Arbitrage Trading Bot

This project is a cryptocurrency arbitrage trading bot that monitors and compares prices across multiple exchanges (Bybit, Binance, Whitebit, Deepcoin) to identify arbitrage opportunities. The bot calculates potential profit percentages and logs profitable trades.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Docker Setup](#docker-setup)
- [Planned Features](#planned-features)

## Introduction

This bot is designed to identify arbitrage opportunities across four cryptocurrency exchanges: Bybit, Binance, Whitebit, and Deepcoin. It calculates potential profit percentages by comparing the bid and ask prices of various trading pairs across these exchanges.

## Features

- **Multi-exchange support**: Works with Bybit, Binance, Whitebit, and Deepcoin.
- **Real-time data fetching**: Continuously monitors trading pairs and calculates potential arbitrage opportunities.
- **Customizable fees**: Allows users to input and adjust trading fees for accurate profit calculation.
- **Dynamic trading volume**: Calculates trade volume based on available liquidity and investment.
- **Performance tracking**: Logs execution time and performance of each arbitrage check.

## Requirements

- Python 3.10+
- Docker (optional, for containerized deployment)
- Pip (Python package installer)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/coin_arbitrage.git
    cd coin_arbitrage
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` file** in the root directory with the following environment variables:

    ```plaintext
    BINANCE_API_KEY=...
    BINANCE_API_SECRET=...
    BYBIT_API_KEY=...
    BYBIT_API_SECRET=...
    ```

## Usage

Run the bot with the following command:

```bash
python main.py
```

### Key Functions

- `get_fees(exchange, symbol, whitebit_symbol_fee)`: Retrieves the trading fees for the specified exchange and trading pair.
- `arbitrage(exchange1, exchange2, data1, data2, symbol, whitebit_symbol_fee)`: Calculates the potential profit from an arbitrage opportunity between two exchanges.
- `arbitrage_check(data1, data2)`: Checks if a potential arbitrage opportunity exists by comparing bid and ask prices.

### Arbitrage Logic

- The bot fetches trading pairs from multiple exchanges.
- It calculates potential arbitrage opportunities by comparing bid and ask prices.
- The bot logs details of each profitable trade, including the profit percentage, trade volume, and prices.
- In info.txt you can see an example of responses to queries used in the code

## Docker Setup

To run the project using Docker:

### Build the Docker image:

```bash
docker build -t arbitrage-bot .
```

### Run the Docker container:

```bash
docker run -d --name arbitrage-bot arbitrage-bot
```
The Docker container will automatically load the environment variables from the .env file and start the bot.

## Planned Features
- Integration with additional cryptocurrency exchanges.
- Implementation of automatic execution of transactions.
- Improved error handling and retry logic for API requests.
- Acquiring new skills in DevOps
- Implementation of Kubernetes
