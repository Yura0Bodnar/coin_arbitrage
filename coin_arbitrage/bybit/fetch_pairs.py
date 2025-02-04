from coin_arbitrage.auxiliary_functions import *

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
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bybit pairs: {e}")
        return []
