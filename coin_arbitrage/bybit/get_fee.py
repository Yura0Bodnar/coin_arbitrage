import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

symbol = 'BTCUSDT'

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
