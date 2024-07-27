import requests


def get_bybit_data(symbol):
    response, data = None, None
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ticker = data['result']['list'][0]
        return {
            "bid_price": float(ticker['bid1Price']),
            "ask_price": float(ticker['ask1Price']),
            "bid_size": float(ticker['bid1Size']),
            "ask_size": float(ticker['ask1Size']),
            "volume_24h": float(ticker['volume24h']),
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bybit data for {symbol}: {e}. Status code: {response.status_code}")
        return None
    except (ValueError, IndexError) as e:
        print(f"Error processing Bybit data for {symbol}: {e}. Status code: {response.status_code}")
        return None
    except KeyError:
        return None


def get_binance_data(symbol):
    response = None
    try:
        url = f"https://api4.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "bid_price": float(data['bidPrice']),
            "ask_price": float(data['askPrice']),
            "bid_size": float(data['bidQty']),
            "ask_size": float(data['askQty']),
            "volume_24h": float(data['volume']),
        }
    except requests.exceptions.RequestException as e:
        if response.status_code == 400:
            return None
        print(f"Error fetching Binance data for {symbol}: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error processing Binance data for {symbol}: {e}")
        return None


def get_okx_data(symbol):
    response = None
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ticker = data['data'][0]
        return {
            "bid_price": float(ticker['bidPx']),
            "ask_price": float(ticker['askPx']),
            "bid_size": float(ticker['bidSz']),
            "ask_size": float(ticker['askSz']),
            "volume_24h": float(ticker['vol24h']),
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OKX data for {symbol}: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error processing OKX data for {symbol}: {e}")
        return None
    except IndexError:
        return None
