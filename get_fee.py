import base64
import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

symbol = 'BTCUSDT'


def get_server_time_binance():
    url = 'https://api.binance.com/api/v3/time'
    response = requests.get(url)
    return response.json()['serverTime']


def get_binance_fee(symbol):
    api_key = os.environ.get('BINANCE_API_KEY')
    api_secret = os.environ.get('BINANCE_API_SECRET')

    server_time = get_server_time_binance()
    timestamp = str(server_time)
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
    print(data)

    taker_fee = float(data['standardCommission']['taker'])
    maker_fee = float(data['standardCommission']['maker'])

    return taker_fee, maker_fee


def get_bybit_fee(symbol):
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
    print(data)
    taker_fee = float(data['result']['list'][0]['takerFeeRate'])
    maker_fee = float(data['result']['list'][0]['makerFeeRate'])

    return taker_fee, maker_fee


def get_okx_fee():
    api_key = os.environ.get('OKX_API_KEY')
    api_secret = os.environ.get('OKX_API_SECRET')
    api_passphrase = os.environ.get('OKX_API_PASSPHRASE')

    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
    method = 'GET'
    request_path = '/api/v5/account/trade-fee?instType=SPOT&instId=BTC-USDT'

    prehash = timestamp + method + request_path
    print('Prehash: ', prehash)
    signature = hmac.new(api_secret.encode('utf-8'), prehash.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(signature).decode()

    headers = {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': api_passphrase,
    }

    response = requests.get(f'https://www.okx.com{request_path}', headers=headers)
    data = response.json()

    print(data)

    taker_fee = float(data['data'][0]['taker'])
    maker_fee = float(data['data'][0]['maker'])

    return taker_fee, maker_fee

