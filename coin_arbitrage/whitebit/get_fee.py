import requests
from dotenv import load_dotenv

load_dotenv()

symbol = 'BTCUSDT'

def get_whitebit_fee(symbol):
    try:
        # URL для отримання інформації про активи
        url = "https://whitebit.com/api/v4/public/assets"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data[symbol])
        # Check for a character in the data
        if symbol in data:
            asset_info = data[symbol]
            taker_fee = float(asset_info.get('taker_fee', 0))
            return taker_fee
        else:
            print(f"Symbol {symbol} not found in the asset data.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except (ValueError, IndexError) as e:
        print(f"Error processing fee data from Whitebit: {e}")
        return None
    except KeyError:
        return None
