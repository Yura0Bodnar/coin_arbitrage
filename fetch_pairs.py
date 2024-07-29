import requests


def fetch_pairs_bybit():
    endpoint = '/v5/market/instruments-info?category=spot'

    try:
        response = requests.get(f'https://api.bybit.com{endpoint}')
        response.raise_for_status()
        data = response.json()

        if 'result' in data and 'list' in data['result']:
            usdt_pairs = [item['symbol'] for item in data['result']['list'] if item['symbol'].endswith('USDT')]
            return usdt_pairs
        else:
            print("Error in response data:", data)
            return []
    except requests.exceptions.RequestException as e:  # Обробка помилок HTTP-запитів
        print(f"Error fetching Bybit pairs: {e}")
        return []


def fetch_pairs_binance():
    endpoint = '/api/v3/exchangeInfo'
    url = f'https://api4.binance.com{endpoint}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        usdt_pairs = [item['symbol'] for item in data['symbols'] if
                      item['symbol'].endswith('USDT') and item['status'] == 'TRADING']
        return usdt_pairs
    except requests.exceptions.RequestException as e:  # Обробка помилок HTTP-запитів
        print(f"Error fetching Binance pairs: {e}")
        return []


def fetch_pairs_whitebit():
    url = f'https://whitebit.com/api/v4/public/markets'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        usdt_pairs = [market['name'] for market in data if market['type'] == 'spot' and market['name'].endswith('USDT')]
        return usdt_pairs
    except requests.exceptions.RequestException as e:  # Обробка помилок HTTP-запитів
        print(f"Error fetching OKX pairs: {e}")
        return []


def fetch_pairs_deepcoin():
    url = "https://api.deepcoin.com/deepcoin/market/instruments?instType=SPOT"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response JSON
        data = response.json()

        # Check if 'data' key exists and contains a list
        if 'data' in data and isinstance(data['data'], list):
            usdt_pairs = [item['instId'] for item in data['data'] if item['quoteCcy'] == 'USDT']
            return usdt_pairs
        else:
            print(f"Unexpected response format: {data}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except (ValueError, KeyError) as e:
        print(f"Error processing data: {e}")
        return []


def association_pairs():
    pairs_bybit = set(fetch_pairs_bybit())
    pairs_binance = set(fetch_pairs_binance())
    pairs_whitebit = set(fetch_pairs_whitebit())
    pairs_deepcoin = set(fetch_pairs_deepcoin())

    # Пошук пар, які є на двох біржах
    common_bybit_binance = pairs_bybit & pairs_binance
    common_binance_whitebit = pairs_binance & pairs_whitebit
    common_bybit_whitebit = pairs_bybit & pairs_whitebit
    common_bybit_deepcoin = pairs_bybit & pairs_deepcoin
    common_binance_deepcoin = pairs_binance & pairs_deepcoin
    common_deepcoin_whitebit = pairs_whitebit & pairs_deepcoin

    # Об'єднання всіх спільних пар в один масив
    common_pairs = common_bybit_binance | common_binance_whitebit | common_bybit_whitebit | common_bybit_deepcoin | common_binance_deepcoin | common_deepcoin_whitebit

    return list(common_pairs)
