import requests

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