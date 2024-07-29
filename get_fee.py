import base64
import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv
import asyncio

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

    except requests.exceptions.RequestException as e:  # Handle HTTP request errors
        print(f"Error fetching Bybit fee for {symbol}: {e}")
        taker_fee = None
    except (ValueError, KeyError, IndexError) as ve:  # Handle unexpected response format errors
        print(f"Error processing response for Bybit fee for {symbol}: {ve}")
        taker_fee = None

    return taker_fee


def get_whitebit_fee(symbol):
    try:
        # URL для отримання інформації про активи
        url = "https://whitebit.com/api/v4/public/assets"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data[symbol])
        # Перевірка наявності символу у даних
        if symbol in data:
            asset_info = data[symbol]
            withdraw_info = asset_info.get('limits', {}).get('withdraw', {}).get(symbol, {})
            deposit_info = asset_info.get('limits', {}).get('deposit', {}).get(symbol, {})

            return {
                "taker_fee": float(asset_info.get('taker_fee', 0)),
                "min_deposit": float(deposit_info.get('min', 0)),
                "min_withdraw": float(withdraw_info.get('min', 0)),
                "can_withdraw": asset_info.get('can_withdraw', False),
                "can_deposit": asset_info.get('can_deposit', False),
                "max_withdraw": float(asset_info.get('max_withdraw', 0)),
                "max_deposit": float(asset_info.get('max_deposit', 0))
            }
        else:
            print(f"Symbol {symbol} not found in the asset data.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error processing data: {e}")
        return None
