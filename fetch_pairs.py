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


def fetch_pairs_okx():
    endpoint = '/api/v5/public/instruments?instType=SPOT'
    url = f'https://www.okx.com{endpoint}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        usdt_pairs = [item['instId'].replace('-', '') for item in data['data'] if item['instId'].endswith('-USDT')]
        return usdt_pairs
    except requests.exceptions.RequestException as e:  # Обробка помилок HTTP-запитів
        print(f"Error fetching OKX pairs: {e}")
        return []


def association_pairs():
    pairs_bybit = set(fetch_pairs_bybit())
    pairs_binance = set(fetch_pairs_binance())
    pairs_okx = set(fetch_pairs_okx())

    # Пошук пар, які є на двох біржах
    common_bybit_binance = pairs_bybit & pairs_binance
    common_binance_okx = pairs_binance & pairs_okx
    common_bybit_okx = pairs_bybit & pairs_okx

    # Об'єднання всіх спільних пар в один масив
    common_pairs = common_bybit_binance | common_binance_okx | common_bybit_okx

    return list(common_pairs)
