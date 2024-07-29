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
    except (KeyError, ValueError) as e:
        print(f"Error processing whitebit data for {symbol}: {e}")
        return None
    except IndexError:
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

        print(f"Symbol {symbol} not found in the response data.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Deepcoin data: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error processing Deepcoin data: {e}")
        return None
