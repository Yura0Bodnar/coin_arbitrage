from coin_arbitrage.auxiliary_functions import *
import redis
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
REDIS_HOST = os.getenv("REDIS_HOST")

# Підключаємо Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

def fetch_pairs_whitebit(redis_key):
    url = f'https://whitebit.com/api/v4/public/markets'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        usdt_pairs = [market['name'] for market in data if market['type'] == 'spot' and market['name'].endswith('USDT')]

        if usdt_pairs:
            redis_client.sadd(redis_key, *usdt_pairs)  # Додаємо унікальні значення в SET
            logging.info(f"Записано {len(usdt_pairs)} пар у Redis під ключем '{redis_key}'")

        return usdt_pairs
    except requests.exceptions.RequestException as e:  # Обробка помилок HTTP-запитів
        logging.error(f"Error fetching OKX pairs: {e}")
        return []