import os
import time
import hmac
import hashlib
import requests
import redis
import logging
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv(".bybit_env")

symbol = "BTCUSDT"

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

REDIS_HOST = os.getenv("REDIS_HOST")

# Підключаємо Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


def get_server_time():
    """
    Отримання поточного часу сервера через ендпоінт /v5/market/time.
    """
    endpoint = "/v5/market/time"
    base_url = "https://api.bybit.com"
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка статусу відповіді
        data = response.json()

        if data["retCode"] == 0:
            # server_time_sec = int(data["result"]["timeSecond"])  # Серверний час у секундах
            server_time_ms = int(data["time"])  # Серверний час у мілісекундах
            return server_time_ms
        else:
            raise ValueError(f"Помилка сервера: {data['retMsg']}")
    except Exception as e:
        raise RuntimeError(f"Не вдалося отримати серверний час: {e}")


def get_bybit_fee(symbol):
    api_key = os.environ.get("BYBIT_API_KEY")
    api_secret = os.environ.get("BYBIT_API_SECRET")

    try:
        server_time = get_server_time()

        # Create query string and signature
        query_string = f"category=spot&symbol={symbol}"
        param_str = f"{server_time}{api_key}{query_string}"
        signature = hmac.new(
            api_secret.encode("utf-8"), param_str.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # Set headers
        headers = {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-TIMESTAMP": str(server_time),
        }

        # Make request
        response = requests.get(
            f"https://api.bybit.com/v5/account/fee-rate?{query_string}", headers=headers
        )
        response.raise_for_status()
        data = response.json()

        # Check rate limit
        limit_status = response.headers.get("X-Bapi-Limit-Status")
        limit_reset_timestamp = response.headers.get("X-Bapi-Limit-Reset-Timestamp")
        if limit_status is not None and int(limit_status) == 0:
            reset_time = int(limit_reset_timestamp) / 1000 - time.time()
            logging.warning(f"Rate limit exceeded. Waiting for {reset_time} seconds.")
            time.sleep(max(reset_time, 0))
            return get_bybit_fee(symbol)

        # Обробка результату
        if "result" in data and "list" in data["result"]:
            taker_fee = float(data["result"]["list"][0]["takerFeeRate"])
        else:
            raise ValueError("Unexpected response format: 'result' or 'list' not found")

        # Формуємо дані для Redis
        fee_data = {
            "taker_fee": taker_fee,
            "timestamp": datetime.now(timezone.utc).isoformat(),  # Додаємо таймстемп
        }

        # Зберігаємо дані в Redis
        redis_key = f"bybit:fee:{symbol}"
        redis_client.hset(redis_key, fee_data)
        logging.info(f"Fee data for {symbol} written to Redis: {fee_data}")

    except requests.exceptions.RequestException as e:  # Handle HTTP request errors
        logging.error(f"Error fetching Bybit fee for {symbol}: {e}")
        taker_fee = None
    except (
        ValueError,
        KeyError,
        IndexError,
    ) as ve:  # Handle unexpected response format errors
        logging.error(f"Error processing response for Bybit fee for {symbol}: {ve}")
        taker_fee = None

    return taker_fee


# fee = get_bybit_fee(symbol)
# if fee is not None:
#     print(f"Taker fee for {symbol}: {fee}")
# else:
#     print("Failed to retrieve Binance fee.")
