import requests
import time


def get_bybit_data():
    url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    ticker = data['result']['list'][0]
    return {
        "bid_price": float(ticker['bid1Price']),
        "ask_price": float(ticker['ask1Price']),
        "volume_24h": float(ticker['volume24h']),
        "timestamp": data['time']
    }


def get_binance_data(symbol):
    url = f"https://api4.binance.com/api/v3/ticker/bookTicker?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return {
        "bid_price": float(data['bidPrice']),
        "ask_price": float(data['askPrice']),
        "volume_24h": None,  # Fetch from another Binance API if needed
        "timestamp": int(time.time() * 1000)
    }
