from get_fee import get_okx_fee, get_binance_fee, get_bybit_fee
from fetch_pairs import association_pairs
from get_data import *
import time

investment = 500


def get_fees(exchange, symbol, symbol_okx):
    if exchange == 'bybit':
        return get_bybit_fee(symbol)
    elif exchange == 'binance':
        return get_binance_fee(symbol)
    elif exchange == 'okx':
        return get_okx_fee(symbol_okx)
    else:
        raise ValueError("Unknown exchange")


def arbitrage(exchange1, exchange2, data1, data2, symbol, symbol_okx):
    bid_price = data1['bid_price']
    ask_price = data2['ask_price']
    bid_size = data1['bid_size']
    ask_size = data2['ask_size']

    fee1 = get_fees(exchange1, symbol, symbol_okx)
    fee2 = get_fees(exchange2, symbol, symbol_okx)

    # Calculate potential profit
    trade_volume = min(investment / ask_price, bid_size, ask_size)
    trade_volume_usdt = trade_volume * bid_price

    sell_revenue = trade_volume * bid_price  # Прибуток від продажу
    buy_cost = trade_volume * ask_price  # Прибуток від купівлі

    potential_profit = sell_revenue - buy_cost  # Прибуток від арбітражу
    net_profit = potential_profit - (buy_cost * fee2 / 100) - (sell_revenue * fee1 / 100)

    profit_percent = (potential_profit / buy_cost) * 100  # Відсоток прибутку

    return net_profit, profit_percent, trade_volume, trade_volume_usdt


def arbitrage_check(data1, data2):
    bid_price = data1['bid_price']
    ask_price = data2['ask_price']
    bid_size = data1['bid_size']
    ask_size = data2['ask_size']

    trade_volume = min(investment / ask_price, bid_size, ask_size)
    buy_cost = trade_volume * ask_price  # скільки ти зможеш купити монет
    sell_revenue = trade_volume * bid_price  # Прибуток від продажу

    potential_profit = sell_revenue - buy_cost  # Прибуток від арбітражу

    # Calculate potential profit
    # spread = bid_price - ask_price  # Дізнатись різницю в ціні
    # profit = bid_size * bid_price - ask_size * ask_price
    # profit_percent = (spread / ask_price) * 100

    return potential_profit


def add_hyphen(symbol):
    return f"{symbol[:-4]}-{symbol[-4:]}"


def main():
    it = 0
    pairs_okx, pairs = None, None
    while True:
        try:
            start_time = time.time()
            if it % 120 == 0:
                pairs = association_pairs()

            for pair in pairs:
                try:
                    okx_pair = add_hyphen(pair)

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
                        if data1 is None or data2 is None:
                            continue
                        else:
                            if (data1['volume_24h'] > 5000000 and data2['volume_24h'] > 5000000
                                    and data1['bid_size'] * data1['bid_price'] >= investment and data2['ask_size'] * data2['ask_price'] >= investment):
                                potential_profit = arbitrage_check(data1, data2)
                                if potential_profit > 5:
                                    profit, profit_percent, trade_volume, trade_volume_usdt = arbitrage(exchange1, exchange2, data1, data2, pair, okx_pair)
                                    print(f"### Arbitrage opportunity {pair} ### \n"
                                          f"Number of coins: {trade_volume}\n"
                                          f"Cost USDT: {trade_volume_usdt}\n"
                                          f"Sell on {exchange1} \n"
                                          f"Buy on {exchange2} \n"
                                          f"Profit: {profit}\n"
                                          f"Percent profit: {profit_percent:.2f}%\n\n")

                except Exception as e:
                    print(f"Error processing pair {pair}: {str(e)}")
                    continue

            it += 1
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            time.sleep(1)  # Затримка для зменшення навантаження на API

        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            time.sleep(60)  # Затримка перед повторною спробою в разі глобальної помилки


if __name__ == "__main__":
    main()
