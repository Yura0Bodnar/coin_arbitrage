import requests


def get_binance_data(symbol):
    response = None
    try:
        url = f"https://api4.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "bid_price": float(data["bidPrice"]),
            "ask_price": float(data["askPrice"]),
            "bid_size": float(data["bidQty"]),
            "ask_size": float(data["askQty"]),
            "volume_24h": float(data["volume"]),
        }
    except requests.exceptions.RequestException as e:
        if response.status_code == 400:
            return None
        print(f"Error fetching Binance data for {symbol}: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error processing Binance data for {symbol}: {e}")
        return None
