import time
import hashlib
import hmac
import requests
import os
from dotenv import load_dotenv

load_dotenv()

symbol = 'BTCUSDT'


def get_bybit_fee():
    api_key = os.environ.get('BYBIT_API_KEY')
    api_secret = os.environ.get('BYBIT_API_SECRET')
    timestamp = str(int(time.time() * 1000))
    recv_window = '5000'
    query_string = f'category=spot&symbol={symbol}'
    param_str = f'{timestamp}{api_key}{recv_window}{query_string}'
    hash = hmac.new(api_secret.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha256)
    signature = hash.hexdigest()

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-TIMESTAMP': timestamp,
        'X-BAPI-RECV-WINDOW': recv_window,
    }

    response = requests.get(f'https://api.bybit.com/v5/account/fee-rate?{query_string}', headers=headers)
    data = response.json()
    taker_fee = float(data['result']['list'][0]['takerFeeRate'])
    maker_fee = float(data['result']['list'][0]['makerFeeRate'])

    return taker_fee, maker_fee


def get_binance_fee():
    api_key = os.environ.get('BINANCE_API_KEY')
    api_secret = os.environ.get('BINANCE_API_SECRET')

    timestamp = str(int(time.time() * 1000))
    query_string = f'symbol={symbol}&timestamp={timestamp}'

    # Генерація підпису
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Заголовки для запиту
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Повний запит з підписом
    url = f'https://api.binance.com/api/v3/account/commission?{query_string}&signature={signature}'
    response = requests.get(url, headers=headers)

    data = response.json()

    taker_fee = float(data['standardCommission']['taker'])
    maker_fee = float(data['standardCommission']['maker'])

    return taker_fee, maker_fee


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


def arbitrage_bybit_to_binance(bybit_data, binance_data):
    bybit_bid = bybit_data['bid_price']
    binance_ask = binance_data['ask_price']

    fee_bybit, _ = get_bybit_fee()
    fee_bin, _ = get_binance_fee()

    # Calculate potential profit
    spread = bybit_bid - binance_ask
    net_profit = spread - (binance_ask * fee_bin / 100) - (bybit_bid * fee_bybit / 100)

    return net_profit


def main():
    bybit_data = get_bybit_data()
    binance_data = get_binance_data(symbol)
    net_profit = arbitrage_bybit_to_binance(bybit_data, binance_data)

    print(f"Net Profit: {net_profit}")


if __name__ == "__main__":
    main()
