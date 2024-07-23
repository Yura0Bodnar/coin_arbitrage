import base64
import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv()

symbol = 'BTCUSDT'


def get_binance_fee(symbol):
    api_key = os.environ.get('BINANCE_API_KEY')
    api_secret = os.environ.get('BINANCE_API_SECRET')

    try:
        time_req = requests.get('https://api.binance.com/api/v3/time')
        time_res = time_req.json()['serverTime']
        server_time = time_res
        timestamp = str(server_time)

        query_string = f'symbol={symbol}&timestamp={timestamp}'

        # Generate signature
        signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        # Headers for the request
        headers = {
            'X-MBX-APIKEY': api_key
        }

        # Full request with signature
        url = f'https://api.binance.com/api/v3/account/commission?{query_string}&signature={signature}'
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if 'standardCommission' in data and 'taker' in data['standardCommission']:
            taker_fee = float(data['standardCommission']['taker'])
        else:
            raise ValueError("Unexpected response format: 'standardCommission' or 'taker' not found")

        return taker_fee

    except requests.exceptions.RequestException as e:  # Handle HTTP request errors
        print(f"Error fetching Binance fee for {symbol}: {e}")
        return None
    except ValueError as ve:  # Handle unexpected response format errors
        print(f"Error processing response for Binance fee for {symbol}: {ve}")
        return None


def get_bybit_fee(symbol):
    api_key = os.environ.get('BYBIT_API_KEY')
    api_secret = os.environ.get('BYBIT_API_SECRET')
    fees = {}

    try:
        # Get server time
        time_req = requests.get('https://api.bybit.com/v2/public/time')
        time_req.raise_for_status()
        time_res = time_req.json()['time_now']
        server_time = str(int(float(time_res) * 1000))

        # Create query string and signature
        query_string = f'category=spot&symbol={symbol}'
        param_str = f'{server_time}{api_key}{query_string}'
        signature = hmac.new(api_secret.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha256).hexdigest()

        # Set headers
        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-TIMESTAMP': server_time,
        }

        # Make request
        response = requests.get(f'https://api.bybit.com/v5/account/fee-rate?{query_string}', headers=headers)
        response.raise_for_status()
        data = response.json()

        # Check rate limit
        limit_status = response.headers.get('X-Bapi-Limit-Status')
        limit_reset_timestamp = response.headers.get('X-Bapi-Limit-Reset-Timestamp')
        if limit_status is not None and int(limit_status) == 0:
            reset_time = int(limit_reset_timestamp) / 1000 - time.time()
            print(f"Rate limit exceeded. Waiting for {reset_time} seconds.")
            time.sleep(max(reset_time, 0))
            return get_bybit_fee(symbol)

        if 'result' in data and 'list' in data['result']:
            taker_fee = float(data['result']['list'][0]['takerFeeRate'])
        else:
            raise ValueError("Unexpected response format: 'result' or 'list' not found")

        fees[symbol] = taker_fee

    except requests.exceptions.RequestException as e:  # Handle HTTP request errors
        print(f"Error fetching Bybit fee for {symbol}: {e}")
        fees[symbol] = None
    except (ValueError, KeyError, IndexError) as ve:  # Handle unexpected response format errors
        print(f"Error processing response for Bybit fee for {symbol}: {ve}")
        fees[symbol] = None

    return fees


def get_okx_fee(symbol):
    api_key = os.environ.get('OKX_API_KEY')
    api_secret = os.environ.get('OKX_API_SECRET')
    api_passphrase = os.environ.get('OKX_API_PASSPHRASE')

    try:
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
        method = 'GET'
        request_path = f'/api/v5/account/trade-fee?instType=SPOT&instId={symbol}'

        prehash = timestamp + method + request_path
        signature = hmac.new(api_secret.encode('utf-8'), prehash.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(signature).decode()

        headers = {
            'OK-ACCESS-KEY': api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': api_passphrase,
        }

        response = requests.get(f'https://www.okx.com{request_path}', headers=headers)
        response.raise_for_status()

        data = response.json()

        if 'data' in data and data['data']:
            taker_fee = float(data['data'][0]['taker'])
        else:
            raise ValueError("Unexpected response format: 'data' not found or empty")

        return abs(taker_fee)

    except requests.exceptions.RequestException as e:  # Обробка помилок HTTP-запитів
        print(f"Error fetching OKX fee for {symbol}: {e}")
        return None
    except ValueError as ve:  # Обробка помилок у випадку неочікуваного формату відповіді
        print(f"Error processing response for OKX fee for {symbol}: {ve}")
        return None


