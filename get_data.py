import requests


def get_bybit_data(symbol):
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ticker = data['result']['list'][0]

        # Ensure all required keys are present in the response
        required_keys = ['bid1Price', 'ask1Price', 'bid1Size', 'ask1Size', 'volume24h']
        if not all(key in ticker for key in required_keys):
            raise KeyError(f"Missing one or more required keys in the response for {symbol}")

        return {
            "bid_price": float(ticker['bid1Price']),
            "ask_price": float(ticker['ask1Price']),
            "bid_size": float(ticker['bid1Size']),
            "ask_size": float(ticker['ask1Size']),
            "volume_24h": float(ticker['volume24h']),
        }
    except requests.exceptions.RequestException as e:
        print(
            f"Error fetching Bybit data for {symbol}: {e}. Status code: {response.status_code if response else 'N/A'}")
        return None
    except (ValueError, IndexError) as e:
        print(f"Error processing Bybit data for {symbol}: {e}. Response data: {data if data else 'N/A'}")
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


def get_whitebit_data(symbol):
    try:
        url_f = f"https://whitebit.com/api/v4/public/orderbook/{symbol}?limit=1"
        url_s = f"https://whitebit.com/api/v4/public/ticker"
        response_f = requests.get(url_f)
        response_s = requests.get(url_s)
        data_f = response_f.json()
        data_s = response_s.json()

        if symbol in data_s:
            return {
                "bid_price": float(data_f['bids'][0][0]),
                "ask_price": float(data_f['asks'][0][0]),
                "bid_size": float(data_f['bids'][0][1]),
                "ask_size": float(data_f['asks'][0][1]),
                "volume_24h": float(data_s[symbol]['quote_volume'])
            }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching whitebit data for {symbol}: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e:
        print(f"Error processing whitebit data for {symbol}: {e}")
        return None


def get_deepcoin_data(symbol):
    try:
        url = "https://api.deepcoin.com/deepcoin/market/tickers?instType=SPOT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Find the specific symbol in the data
        for ticker in data['data']:
            if ticker['instId'] == symbol:
                return {
                    "ask_price": float(ticker['askPx']),
                    "ask_size": float(ticker['askSz']),
                    "bid_price": float(ticker['bidPx']),
                    "bid_size": float(ticker['bidSz']),
                    "volume_24h": float(ticker['vol24h']),
                }

        # If the symbol is not found, return None without any message
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Deepcoin data: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e:
        print(f"Error processing Deepcoin data: {e}")
        return None
