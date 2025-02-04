import os
import hmac
import hashlib
import requests
from dotenv import load_dotenv

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