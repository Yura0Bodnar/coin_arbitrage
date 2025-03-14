import sys
import os
import requests
import redis
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ініціалізація клієнта Redis
REDIS_HOST = os.getenv("REDIS_HOST")

# Підключаємо Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


def get_bybit_data(symbol, redis_key):
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        ticker = data["result"]["list"][0]

        # Ensure all required keys are present in the response
        required_keys = ["bid1Price", "ask1Price", "bid1Size", "ask1Size", "volume24h"]
        if not all(key in ticker for key in required_keys):
            raise KeyError(
                f"Missing one or more required keys in the response for {symbol}"
            )

        # Формуємо дані
        formatted_data = {
            "bid_price": float(ticker["bid1Price"]),
            "ask_price": float(ticker["ask1Price"]),
            "bid_size": float(ticker["bid1Size"]),
            "ask_size": float(ticker["ask1Size"]),
            "volume_24h": float(ticker["volume24h"]),
        }

        # Записуємо дані в Redis
        redis_client.hset(redis_key, mapping=formatted_data)
        logging.info(f"Data from bybit {symbol} written to Redis: {formatted_data}")

        return formatted_data
    except requests.exceptions.RequestException as e:
        logging.error(
            f"Error fetching Bybit data for {symbol}: {e}. Status code: {response.status_code if response else 'N/A'}"
        )
        sys.exit(1)
    except (ValueError, IndexError) as e:
        logging.error(
            f"Error processing Bybit data for {symbol}: {e}. Response data: {data if data else 'N/A'}"
        )
        sys.exit(1)
    except KeyError:
        logging.error(f"Missing keys in Bybit data for {symbol}.")
        sys.exit(1)
