import redis
import requests
import logging
import sys
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

REDIS_HOST = os.getenv("REDIS_HOST")

# Підключаємо Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


def get_whitebit_data(symbol, redis_key):
    try:
        url_orderbook = f"https://whitebit.com/api/v4/public/orderbook/{symbol}?limit=1"
        url_ticker = "https://whitebit.com/api/v4/public/ticker"

        response_orderbook = requests.get(url_orderbook, timeout=10)
        response_orderbook.raise_for_status()
        data_orderbook = response_orderbook.json()

        response_ticker = requests.get(url_ticker, timeout=10)
        response_ticker.raise_for_status()
        data_ticker = response_ticker.json()

        # Перевірка, чи є символ у відповіді
        if symbol not in data_ticker:
            raise KeyError(f"Missing data for {symbol} in WhiteBit response")

        # Перевіряємо, чи всі потрібні ключі є в відповіді
        required_keys = ["bids", "asks"]
        if not all(key in data_orderbook for key in required_keys):
            raise KeyError(f"Missing orderbook keys for {symbol}")

        required_ticker_keys = ["quote_volume"]
        if not all(key in data_ticker[symbol] for key in required_ticker_keys):
            raise KeyError(f"Missing ticker keys for {symbol}")

        # Форматуємо отримані дані
        formatted_data = {
            "bid_price": float(data_orderbook["bids"][0][0]),
            "ask_price": float(data_orderbook["asks"][0][0]),
            "bid_size": float(data_orderbook["bids"][0][1]),
            "ask_size": float(data_orderbook["asks"][0][1]),
            "volume_24h": float(data_ticker[symbol]["quote_volume"]),
        }

        # Записуємо дані в Redis
        redis_client.hset(redis_key, mapping=formatted_data)

        logging.info(f"Data from whitebit {symbol} written to Redis: {formatted_data}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching WhiteBit data for {symbol}: {e}.")
        sys.exit(1)
    except (ValueError, IndexError) as e:
        logging.error(
            f"Error processing WhiteBit data for {symbol}: {e}. Response data: "
            f"{data_orderbook if data_orderbook else 'N/A'}"
        )
        sys.exit(1)
    except KeyError as e:
        logging.error(f"Missing keys in WhiteBit data for {symbol}: {e}")
        sys.exit(1)
