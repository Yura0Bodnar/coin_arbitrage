import requests
import time
from whitebit.fetch_pairs import fetch_pairs_whitebit
from binance.fetch_pairs import fetch_pairs_binance
from bybit.fetch_pairs import fetch_pairs_bybit

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
        print(f"Average response time over {num_requests} requests: {avg_time:.4f} seconds")
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
            if not info['can_withdraw'] or not info['can_deposit']:
                restricted_symbols.append(symbol)

        return restricted_symbols

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Whitebit: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error processing data: {e}")
        return None
    
def association_pairs():
    pairs_bybit = set(fetch_pairs_bybit())
    pairs_binance = set(fetch_pairs_binance())
    pairs_whitebit = set(fetch_pairs_whitebit())

    # Removes extra characters to compare pairs on different exchanges
    pairs_whitebit = remove_symbol(pairs_whitebit)

    # Search for pairs that are available on two exchanges
    common_bybit_binance = pairs_bybit & pairs_binance
    common_binance_whitebit = pairs_binance & pairs_whitebit
    common_bybit_whitebit = pairs_bybit & pairs_whitebit

    # Combining all common pairs into one array
    common_pairs = common_bybit_binance | common_binance_whitebit | common_bybit_whitebit

    return list(common_pairs)
