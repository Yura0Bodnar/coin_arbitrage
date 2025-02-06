from coin_arbitrage.whitebit.get_data import get_whitebit_data
from coin_arbitrage.bybit.get_data import get_bybit_data
from coin_arbitrage.auxiliary_functions import association_pairs, add_underline, pair_to_symbol
import logging
import redis
from dotenv import load_dotenv
import os
import time
import sys

# Завантажуємо змінні оточення
load_dotenv()

EXCHANGE_ROLE = os.getenv("EXCHANGE_ROLE")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Підключення до Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def process_bybit():
    """Логіка для контейнера Bybit."""
    while True:
        pairs = redis_client.smembers("bybit:usdt_pairs")
        if not pairs:
            logging.info("Немає пар для обробки Bybit. Очікування...")
            time.sleep(5)
            continue

        for pair in pairs:
            redis_key = f"bybit:{pair}"
            get_bybit_data(pair, redis_key)
            logging.info(f"✅ Дані для {pair} з Bybit записані в Redis")
        time.sleep(10)


def process_whitebit():
    """Логіка для контейнера WhiteBit."""
    while True:
        pairs = redis_client.smembers("whitebit:usdt_pairs")
        if not pairs:
            logging.info("Немає пар для обробки WhiteBit. Очікування...")
            time.sleep(5)
            continue

        for pair in pairs:
            underline_pair = add_underline(pair)
            redis_key = f"whitebit:{underline_pair}"
            get_whitebit_data(underline_pair, redis_key)
            logging.info(f"✅ Дані для {pair} з WhiteBit записані в Redis")
        time.sleep(10)


def main():
    logging.info("Запуск головного процесу")
    it = 0
    pairs = None

    while True:
        start_time = time.time()

        # Оновлюємо список пар кожні 120 ітерацій
        if it % 120 == 0:
            pairs = association_pairs()
            logging.info("Оновлено список USDT пар")
            print(pairs)
        for pair in pairs:
            logging.info(f"Перевіряємо арбітраж для пари: {pair}")
            underline_pair = add_underline(pair)

            signal_bybit = f"bybit:{pair}:ready"
            signal_whitebit = f"whitebit:{underline_pair}:ready"
            bybit_key = f"bybit:{pair}"
            whitebit_key = f"whitebit:{pair}"

            if EXCHANGE_ROLE == "bybit":
                get_bybit_data(pair, bybit_key)
            elif EXCHANGE_ROLE == "whitebit":
                get_whitebit_data(underline_pair, whitebit_key)
            elif EXCHANGE_ROLE == "main":
                # Очікуємо сигналів готовності від контейнерів
                while not (redis_client.get(signal_bybit) and redis_client.get(signal_whitebit)):
                    logging.info(f"Очікуємо дані для {pair} з Bybit і WhiteBit...")
                    time.sleep(5)

                logging.info(f"✅ Отримано сигнали готовності для {pair}. Продовжуємо...")

        if EXCHANGE_ROLE == "main":
            it += 1
            end_time = time.time()
            logging.info(f"Час виконання: {end_time - start_time:.2f} секунд")
            time.sleep(1)


if __name__ == "__main__":
    main()
