import hmac
import requests
import hashlib


def fetch_pairs_bybit():
    endpoint = '/v5/market/instruments-info?category=spot'

    response = requests.get(f'https://api.bybit.com{endpoint}')
    data = response.json()

    if 'result' in data and 'list' in data['result']:
        usdt_pairs = [item['symbol'] for item in data['result']['list'] if item['symbol'].endswith('USDT')]
        return usdt_pairs
    else:
        print("Error in response data:", data)
        return []


def fetch_pairs_binance():
    endpoint = '/api/v3/exchangeInfo'
    url = f'https://api4.binance.com{endpoint}'

    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        usdt_pairs = [item['symbol'] for item in data['symbols'] if
                      item['symbol'].endswith('USDT') and item['status'] == 'TRADING']
        return usdt_pairs
    else:
        print("Error in response data:", data)
        return []


def fetch_pairs_okx():
    endpoint = '/api/v5/public/instruments?instType=SPOT'
    url = f'https://www.okx.com{endpoint}'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        usdt_pairs = [item['instId'].replace('-', '') for item in data['data'] if item['instId'].endswith('-USDT')]
        return usdt_pairs
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return []


def association_pairs():
    pairs_binance = set(fetch_pairs_binance())
    pairs_bybit = set(fetch_pairs_bybit())
    pairs_okx = set(fetch_pairs_okx())

    common_pairs = pairs_binance & pairs_bybit & pairs_okx  # Перетин множин для знаходження спільних елементів

    return list(common_pairs)
