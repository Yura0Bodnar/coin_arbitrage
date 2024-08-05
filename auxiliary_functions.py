import requests
import time


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