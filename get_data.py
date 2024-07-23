import requests


def get_bybit_data(symbol):
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ticker = data['result']['list'][0]
        return {
            "bid_price": float(ticker['bid1Price']),
            "ask_price": float(ticker['ask1Price'])
        }
    except requests.exceptions.RequestException as e:   # Обробка помилок HTTP-запитів
        print(f"Error fetching Bybit data for {symbol}: {e}")
        return {"bid_price": None, "ask_price": None}
    except (KeyError, IndexError, ValueError) as e:  # Обробка помилок у випадку неочікуваного формату відповіді
        print(f"Error processing Bybit data for {symbol}: {e}")
        return {"bid_price": None, "ask_price": None}


def get_binance_data(symbol):
    try:
        url = f"https://api4.binance.com/api/v3/ticker/bookTicker?symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "bid_price": float(data['bidPrice']),
            "ask_price": float(data['askPrice'])
        }
    except requests.exceptions.RequestException as e:   # Обробка помилок HTTP-запитів
        print(f"Error fetching Binance data for {symbol}: {e}")
        return {"bid_price": None, "ask_price": None}
    except (KeyError, ValueError) as e:   # Обробка помилок у випадку неочікуваного формату відповіді
        print(f"Error processing Binance data for {symbol}: {e}")
        return {"bid_price": None, "ask_price": None}


def get_okx_data(symbol='BTC-USDT'):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ticker = data['data'][0]
        return {
            "bid_price": float(ticker['bidPx']),
            "ask_price": float(ticker['askPx']),
        }
    except requests.exceptions.RequestException as e:   # Обробка помилок HTTP-запитів
        print(f"Error fetching OKX data for {symbol}: {e}")
        return {"bid_price": None, "ask_price": None}
    except (KeyError, IndexError, ValueError) as e:   # Обробка помилок у випадку неочікуваного формату відповіді
        print(f"Error processing OKX data for {symbol}: {e}")
        return {"bid_price": None, "ask_price": None}
