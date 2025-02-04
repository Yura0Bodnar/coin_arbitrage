import requests

def get_bybit_data(symbol):
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ticker = data['result']['list'][0]

        # Ensure all required keys are present in the response
        required_keys = ['bid1Price', 'ask1Price', 'bid1Size', 'ask1Size', 'volume24h']
        if not all(key in ticker for key in required_keys):
            raise KeyError(f"Missing one or more required keys in the response for {symbol}")

        return {
            "bid_price": float(ticker['bid1Price']),
            "ask_price": float(ticker['ask1Price']),
            "bid_size": float(ticker['bid1Size']),
            "ask_size": float(ticker['ask1Size']),
            "volume_24h": float(ticker['volume24h']),
        }
    except requests.exceptions.RequestException as e:
        print(
            f"Error fetching Bybit data for {symbol}: {e}. Status code: {response.status_code if response else 'N/A'}")
        return None
    except (ValueError, IndexError) as e:
        print(f"Error processing Bybit data for {symbol}: {e}. Response data: {data if data else 'N/A'}")
        return None
    except KeyError:
        return None
