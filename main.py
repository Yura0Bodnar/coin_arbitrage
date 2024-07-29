from get_fee import *
from fetch_pairs import *
from get_data import *
import time

investment = 500


def get_fees(exchange, symbol, whitebit_symbol_fee):
    if exchange == 'bybit':
        return get_bybit_fee(symbol)
    elif exchange == 'binance':
        return get_binance_fee(symbol)
    elif exchange == 'whitebit':
        return get_whitebit_fee(whitebit_symbol_fee)
    elif exchange == 'deepcoin':
        return 0.06
    else:
        raise ValueError("Unknown exchange")


def arbitrage(exchange1, exchange2, data1, data2, symbol, whitebit_symbol_fee):
    bid_price = data1['bid_price']
    ask_price = data2['ask_price']
    bid_size = data1['bid_size']
    ask_size = data2['ask_size']

    fee1 = get_fees(exchange1, symbol, whitebit_symbol_fee)
    fee2 = get_fees(exchange2, symbol, whitebit_symbol_fee)

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

    return potential_profit


def add_hyphen(symbol):
    return f"{symbol[:-4]}-{symbol[-4:]}"


def add_underline(symbol):
    return f"{symbol[:-4]}-{symbol[-4:]}"


def pair_to_symbol(symbol):
    return f"{symbol[:-5]}"


def test_api_speed(url, num_requests=100):
    times = []
    for _ in range(num_requests):
        start_time = time.time()
        response = requests.get(url)
        elapsed_time = time.time() - start_time
        if response.status_code == 200:
            times.append(elapsed_time)
        else:
            print(f"Request failed with status code {response.status_code}")

    if times:
        avg_time = sum(times) / len(times)
        print(f"Average response time over {num_requests} requests: {avg_time:.4f} seconds")
    else:
        print("No successful requests to calculate speed.")


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
                    whitebit_pair = add_underline(pair)
                    deepcoin_pair = add_hyphen(pair)
                    whitebit_symbol_fee = pair_to_symbol(symbol)

                    bybit_data = get_bybit_data(pair)
                    binance_data = get_binance_data(pair)
                    whitebit_data = get_whitebit_data(whitebit_pair)
                    deepcoin_data = get_deepcoin_data(deepcoin_pair)

                    arbitrages = [
                        ('bybit', 'binance', bybit_data, binance_data),
                        ('binance', 'bybit', binance_data, bybit_data),
                        ('whitebit', 'bybit', whitebit_data, bybit_data),
                        ('whitebit', 'binance', whitebit_data, binance_data),
                        ('bybit', 'whitebit', bybit_data, whitebit_data),
                        ('binance', 'whitebit', binance_data, whitebit_data),
                        ('bybit', 'deepcoin', bybit_data, deepcoin_data),
                        ('binance', 'deepcoin', binance_data, deepcoin_data),
                        ('whitebit', 'deepcoin', whitebit_data, deepcoin_data),
                        ('deepcoin', 'bybit', deepcoin_data, bybit_data),
                        ('deepcoin', 'binance', deepcoin_data, binance_data),
                        ('deepcoin', 'whitebit', deepcoin_data, whitebit_data)
                    ]

                    for exchange1, exchange2, data1, data2 in arbitrages:
                        sell_cost = data1['bid_size'] * data1['bid_price']
                        buy_cost = data2['ask_size'] * data2['ask_price']
                        if data1 is None or data2 is None:
                            continue
                        else:
                            if (data1['volume_24h'] > 5000000 and data2['volume_24h'] > 5000000
                                    and buy_cost >= investment and sell_cost >= investment):
                                potential_profit = arbitrage_check(data1, data2)
                                if potential_profit > 5:
                                    profit, profit_percent, trade_volume, trade_volume_usdt = arbitrage(exchange1, exchange2, data1, data2, pair, whitebit_symbol_fee)
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
