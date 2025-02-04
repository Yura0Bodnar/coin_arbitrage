from coin_arbitrage.auxiliary_functions import *

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
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Binance pairs: {e}")
        return []