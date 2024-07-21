import requests


def get_bybit_data(symbol):
    url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    ticker = data['result']['list'][0]
    return {
        "bid_price": float(ticker['bid1Price']),
        "ask_price": float(ticker['ask1Price'])
    }


def get_binance_data(symbol):
    url = f"https://api4.binance.com/api/v3/ticker/bookTicker?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return {
        "bid_price": float(data['bidPrice']),
        "ask_price": float(data['askPrice'])
    }


def get_okx_data(symbol='BTC-USDT'):
    url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"
    response = requests.get(url)
    data = response.json()
    ticker = data['data'][0]
    return {
        "bid_price": float(ticker['bidPx']),
        "ask_price": float(ticker['askPx']),
    }
