import os
import requests
import redis
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

REDIS_HOST = os.getenv("REDIS_HOST")

# Підключаємо Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


def fetch_pairs_bybit(redis_key):
    """
    Отримує список USDT-пар з Bybit API, зберігає в Redis (SET) та повертає.
    """

    endpoint = "/v5/market/instruments-info?category=spot"
    try:
        response = requests.get(f"https://api.bybit.com{endpoint}")
        response.raise_for_status()
        data = response.json()

        if "result" in data and "list" in data["result"]:
            usdt_pairs = [
                item["symbol"]
                for item in data["result"]["list"]
                if item["symbol"].endswith("USDT")
            ]

            if usdt_pairs:
                redis_client.sadd(
                    redis_key, *usdt_pairs
                )  # Додаємо унікальні значення в SET
                logging.info(
                    f"Записано {len(usdt_pairs)} пар у Redis під ключем '{redis_key}'"
                )

            return usdt_pairs
        else:
            logging.error("Error in response data:", data)
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Bybit pairs: {e}")
        return []
