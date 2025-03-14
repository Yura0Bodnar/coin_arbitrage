import requests
from dotenv import load_dotenv
import redis
from datetime import datetime, timezone
import logging
import os

load_dotenv()

symbol = "BTC"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

REDIS_HOST = os.getenv("REDIS_HOST")
# Підключаємо Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


def get_whitebit_fee(symbol):
    try:
        # URL для отримання інформації про активи
        url = "https://whitebit.com/api/v4/public/assets"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Check for a character in the data
        if symbol in data:
            asset_info = data[symbol]
            taker_fee = float(asset_info.get("taker_fee", 0))

            fee_data = {
                "taker_fee": taker_fee,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),  # Додаємо таймстемп
            }

            redis_key = f"whitebit:fee:{symbol}"
            redis_client.hset(redis_key, fee_data)
            logging.info(f"Fee data for {symbol} written to Redis: {fee_data}")

            return taker_fee
        else:
            logging.error(f"Symbol {symbol} not found in the asset data.")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None
    except (ValueError, IndexError) as e:
        logging.error(f"Error processing fee data from Whitebit: {e}")
        return None
    except KeyError:
        return None


# fee = get_whitebit_fee(symbol)
# if fee is not None:
#     print(f"Taker fee for {symbol}: {fee}")
# else:
#     print("Failed to retrieve Whitebit fee.")
