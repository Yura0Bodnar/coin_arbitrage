import requests
import time
from datetime import datetime, timezone
import logging
import redis
import os
from bybit.fetch_pairs import fetch_pairs_bybit
from whitebit.fetch_pairs import fetch_pairs_whitebit
from coin_arbitrage.whitebit.get_fee import get_whitebit_fee
from coin_arbitrage.bybit.get_fee import get_bybit_fee
import sys

EXCHANGE_ROLE = os.getenv("EXCHANGE_ROLE")  # Docker змінна для ролі контейнера

investment = 1000
REDIS_HOST = os.getenv("REDIS_HOST")

# Підключаємо Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def add_hyphen(pair):
    return f"{pair[:-4]}-{pair[-4:]}"


def add_underline(pair):
    return f"{pair[:-4]}_{pair[-4:]}"


def pair_to_symbol(pair):
    return f"{pair[:-5]}"


def remove_symbol(pairs):
    arr = []
    for pair in pairs:
        pair = pair.replace("-", "").replace("_", "")
        arr.append(pair)
    return set(arr)


def test_api_speed(url, num_requests=100):
    times = []
    for _ in range(num_requests):
        start_time = time.time()
        response = requests.get(url)
        elapsed_time = time.time() - start_time
        if response.status_code == 200:
            times.append(elapsed_time)
        else:
            print(f"Request failed with status code {response.status_code}")

    if times:
        avg_time = sum(times) / len(times)
        print(
            f"Average response time over {num_requests} "
            f"requests: {avg_time:.4f} seconds"
        )
    else:
        print("No successful requests to calculate speed.")


def get_symbols_with_restrictions():
    try:
        url = "https://whitebit.com/api/v4/public/assets"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        restricted_symbols = []
        for symbol, info in data.items():
            if not info["can_withdraw"] or not info["can_deposit"]:
                restricted_symbols.append(symbol)

        return restricted_symbols

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Whitebit: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error processing data: {e}")
        return None


def association_pairs(pairs_key):
    """
    Отримує пари USDT з Redis, порівнює між біржами та повертає список спільних пар.
    """
    redis_key_bybit = "bybit:usdt_pairs"
    redis_key_whitebit = "whitebit:usdt_pairs"
    signal_bybit = "bybit:ready"
    signal_whitebit = "whitebit:ready"

    # Якщо контейнер Bybit, записуємо тільки його дані в Redis
    if EXCHANGE_ROLE == "bybit":
        fetch_pairs_bybit(redis_key_bybit)
        logging.info("Контейнер Bybit оновив свої пари в Redis")
        redis_client.set(signal_bybit, "1")  # Ставимо сигнал готовності для Bybit
        while not redis_client.scard(pairs_key):
            logging.info(f"BYBIT: Очікуємо ключ {pairs_key} у Redis...")
            time.sleep(5)  # Чекаємо 5 секунд перед перевіркою

    # Якщо контейнер WhiteBit, записуємо тільки його дані в Redis
    if EXCHANGE_ROLE == "whitebit":
        fetch_pairs_whitebit(redis_key_whitebit)
        logging.info("Контейнер WhiteBit оновив свої пари в Redis")
        redis_client.set(signal_whitebit, "1")  # Ставимо сигнал готовності для WhiteBit
        while not redis_client.scard(pairs_key):
            logging.info(f"WHITEBIT: Очікуємо ключ {pairs_key} у Redis...")
            time.sleep(5)  # Чекаємо 5 секунд перед перевіркою

    # Якщо контейнер Main, то чекаємо сигналів від Bybit і WhiteBit
    if EXCHANGE_ROLE == "main":
        while not (
            redis_client.get(signal_bybit) and redis_client.get(signal_whitebit)
        ):
            logging.info("Очікуємо оновлення даних від Bybit та WhiteBit...")
            time.sleep(5)  # Чекаємо 5 секунд перед перевіркою

        logging.info(
            "Отримано сигнали готовності від Bybit та WhiteBit. Продовжуємо..."
        )

        pairs_bybit = redis_client.smembers(redis_key_bybit)
        pairs_whitebit = redis_client.smembers(redis_key_whitebit)

        if not pairs_bybit:
            logging.warning("Дані Bybit відсутні у Redis. Зупинка програми")
            return []

        if not pairs_whitebit:
            logging.warning("Дані WhiteBit відсутні у Redis. Зупинка програми")
            return []

        # Видаляємо зайві символи для уніфікації назв пар на WhiteBit
        pairs_whitebit = remove_symbol(pairs_whitebit)

        # Знаходимо спільні пари між Bybit та WhiteBit
        common_pairs = pairs_bybit & pairs_whitebit

        logging.info(f"Знайдено {len(common_pairs)} спільних пар між Bybit та WhiteBit")

        # Видаляємо дані про пари з Redis після обробки (тільки якщо це головний контейнер)
        redis_client.delete(redis_key_bybit)
        redis_client.delete(redis_key_whitebit)

        redis_client.delete(signal_bybit)
        redis_client.delete(signal_whitebit)
        redis_client.sadd(pairs_key, *common_pairs)
        time.sleep(5)
        logging.info(
            f"Видалено ключі: {redis_key_bybit}, {redis_key_whitebit}, {signal_bybit}, {signal_whitebit} з Redis"
        )


def get_fees(exchange, symbol, whitebit_symbol_fee):
    """
    Отримує комісію з Redis або API (кеш оновлюється кожну годину).
    """
    redis_key = f"{exchange}:fee:{symbol}"
    cached_fee = redis_client.hgetall(redis_key)

    # Якщо кеш є, перевіряємо час
    if cached_fee:
        timestamp = datetime.fromisoformat(cached_fee["timestamp"]).replace(
            tzinfo=timezone.utc
        )
        if (datetime.now(timezone.utc) - timestamp).total_seconds() < 3600:
            return float(cached_fee["taker_fee"])  # Повертаємо кешовану комісію

        # Видаляємо старий запис, якщо час минув
        redis_client.delete(redis_key)

    # Якщо кешу немає або він застарів – отримуємо нові дані
    logging.info(f"Отримуємо комісію для {exchange}, {symbol}")
    if exchange == "bybit":
        taker_fee = get_bybit_fee(symbol)
    elif exchange == "whitebit":
        taker_fee = get_whitebit_fee(whitebit_symbol_fee)
    else:
        logging.error("Unknown exchange")
        raise ValueError("Unknown exchange")

    return taker_fee


def arbitrage(exchange1, exchange2, symbol, whitebit_symbol_fee):
    """
    Виконує арбітраж, використовуючи дані з Redis.
    """
    logging.info(f"Виконуємо арбітраж між {exchange1} та {exchange2} для {symbol}")

    # Отримуємо дані з Redis
    data1 = redis_client.hgetall(f"{exchange1}:{symbol}")
    data2 = redis_client.hgetall(f"{exchange2}:{symbol}")

    if not data1 or not data2:
        logging.error(f"❌ Дані відсутні в Redis для {exchange1} або {exchange2}")
        return None, None, None, None, None, None

    # Конвертуємо дані у float
    data1 = {k: float(v) for k, v in data1.items()}
    data2 = {k: float(v) for k, v in data2.items()}

    bid_price = data1["bid_price"]
    ask_price = data2["ask_price"]
    bid_size = data1["bid_size"]
    ask_size = data2["ask_size"]

    # Отримуємо комісію, доки не отримаємо валідні значення
    fee1, fee2 = None, None
    a, b = 0, 0
    while not (a == 1 and b == 1):
        try:
            if fee1 is None and exchange1 == "bybit":
                fee1 = get_fees(exchange1, symbol, whitebit_symbol_fee)
                if fee1 is not None:
                    logging.info(
                        f"✅ Отримано комісію від {exchange1} для {symbol}: {fee1}"
                    )
                    a = 1
                else:
                    raise ValueError(
                        f"❌ Не вдалося отримати `taker_fee` для {exchange1}"
                    )

            if fee2 is None and exchange2 == "whitebit":
                fee2 = get_fees(exchange2, symbol, whitebit_symbol_fee)
                if fee2 is not None:
                    logging.info(
                        f"✅ Отримано комісію від {exchange2} для {symbol}: {fee2}"
                    )
                    b = 1
                else:
                    raise ValueError(
                        f"❌ Не вдалося отримати `taker_fee` для {exchange2}"
                    )

        except Exception as e:
            logging.error(f"❌ Помилка при отриманні комісії: {e}")
            sys.exit(1)  # Завершення скрипту у разі невдачі

    logging.info("✅ Успішно отримано `taker_fee` з 2 бірж, продовжуємо арбітраж")

    trade_volume = min(investment / ask_price, bid_size, ask_size)
    trade_volume_usdt = trade_volume * bid_price

    sell_revenue = trade_volume * bid_price
    buy_cost = trade_volume * ask_price

    potential_profit = sell_revenue - buy_cost
    net_profit = (
        potential_profit - (buy_cost * fee2 / 100) - (sell_revenue * fee1 / 100)
    )

    profit_percent = (potential_profit / buy_cost) * 100

    logging.info(f"✅ Арбітраж завершено між {exchange1} та {exchange2} для {symbol}")

    # Видаляємо дані про пари з Redis після обробки
    redis_client.delete(f"{exchange1}:{symbol}")
    redis_client.delete(f"{exchange2}:{symbol}")
    logging.info(
        f"🗑 Видалено ключі: {exchange1}:{symbol}, {exchange2}:{symbol} з Redis"
    )

    return (
        net_profit,
        profit_percent,
        trade_volume,
        trade_volume_usdt,
        bid_price,
        ask_price,
    )
