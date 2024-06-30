from get_data import get_bybit_data, get_binance_data
from calculate_data import arbitrage_bybit_to_binance, arbitrage_binance_to_bybit

symbol = 'BTCUSDT'


def main():
    bybit_data = get_bybit_data()
    binance_data = get_binance_data(symbol)
    net_profit_1 = arbitrage_bybit_to_binance(bybit_data, binance_data)
    net_profit_2 = arbitrage_binance_to_bybit(bybit_data, binance_data)

    print(f"Net Profit from bybit to binance: {net_profit_1}")
    print(f"Net Profit from binance to bybit: {net_profit_2}")


if __name__ == "__main__":
    main()
