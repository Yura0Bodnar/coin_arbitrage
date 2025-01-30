from coin_arbitrage.auxiliary_functions import *

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