from dotenv import load_dotenv
from get_fee import get_okx_fee, get_binance_fee, get_bybit_fee
from fetch_pairs import association_pairs
from get_data import *
import os
import time

load_dotenv()
symbol = 'BTCUSDT'

# Отримання змінних середовища
api_key = os.environ.get('BYBIT_API_KEY')
api_secret = os.environ.get('BYBIT_API_SECRET')


def get_fees(exchange, symbol, fee_bybit, fee_binance, fee_okx):
    if exchange == 'bybit':
        return fee_bybit[symbol]
    elif exchange == 'binance':
        return fee_binance[symbol]
    elif exchange == 'okx':
        return fee_okx[symbol]
    else:
        raise ValueError("Unknown exchange")


def arbitrage(exchange1, exchange2, data1, data2, fee_bybit, fee_binance, fee_okx):
    bid_price = data1['bid_price']
    ask_price = data2['ask_price']

    fee1 = get_fees(exchange1, symbol, fee_bybit, fee_binance, fee_okx)
    fee2 = get_fees(exchange2, symbol, fee_bybit, fee_binance, fee_okx)

    # Calculate potential profit
    spread = bid_price - ask_price
    net_profit = spread - (ask_price * fee2 / 100) - (bid_price * fee1 / 100)
    profit_percent = (net_profit / ask_price) * 100

    return profit_percent


def add_hyphen_okx(pairs):
    formatted_pairs = []
    for pair in pairs:
        begin = pair[:-4]
        end = "USDT"
        formatted_pairs.append(f"{begin}-{end}")

    return formatted_pairs


def main():
    it = 0
    pairs_okx, pairs = None, None
    fee_bybit, fee_binance, fee_okx = {}, {}, {}
    while True:
        try:
            if it % 120 == 0:
                pairs = association_pairs()
                pairs_okx = add_hyphen_okx(pairs)
            if it % 800 == 0:
                fee_bybit = {pair: get_bybit_fee(pair) for pair in pairs}
                fee_binance = {pair: get_binance_fee(pair) for pair in pairs}
                fee_okx = {pair: get_okx_fee(pair) for pair in pairs_okx}

            for pair, okx_pair in zip(pairs, pairs_okx):
                try:
                    bybit_data = get_bybit_data(pair)
                    binance_data = get_binance_data(pair)
                    okx_data = get_okx_data(okx_pair)

                    arbitrages = [
                        ('bybit', 'binance', bybit_data, binance_data),
                        ('binance', 'bybit', binance_data, bybit_data),
                        ('okx', 'bybit', okx_data, bybit_data),
                        ('okx', 'binance', okx_data, binance_data),
                        ('bybit', 'okx', bybit_data, okx_data),
                        ('binance', 'okx', binance_data, okx_data)
                    ]

                    for exchange1, exchange2, data1, data2 in arbitrages:
                        profit_percent = arbitrage(exchange1, exchange2, data1, data2, fee_bybit[pair],
                                                   fee_binance[pair], fee_okx[okx_pair])
                        if profit_percent > 0.5:
                            print(
                                f"### Arbitrage opportunity {pair} ### \nSell on {exchange1} \nBuy on {exchange2} \nPotential profit: {profit_percent:.2f}%")

                except Exception as e:
                    print(f"Error processing pair {pair}: {str(e)}")
                    continue

            it += 1
            time.sleep(1)  # Затримка для зменшення навантаження на API

        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            time.sleep(60)  # Затримка перед повторною спробою в разі глобальної помилки


if __name__ == "__main__":
    main()
