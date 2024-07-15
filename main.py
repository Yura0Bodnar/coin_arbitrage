from get_data import get_bybit_data, get_binance_data, get_okx_data
from get_fee import get_okx_fee, get_binance_fee, get_bybit_fee

symbol = 'BTCUSDT'


def get_fees(exchange, symbol, it):
    if exchange == 'bybit':
        return get_bybit_fee(symbol, it)
    elif exchange == 'binance':
        return get_binance_fee(symbol, it)
    elif exchange == 'okx':
        return get_okx_fee(symbol, it)
    else:
        raise ValueError("Unknown exchange")


def arbitrage(exchange1, exchange2, data1, data2, it):
    bid_price = data1['bid_price']
    ask_price = data2['ask_price']

    fee1, _ = get_fees(exchange1, symbol, it)
    fee2, _ = get_fees(exchange2, symbol, it)

    # Calculate potential profit
    spread = bid_price - ask_price
    net_profit = spread - (ask_price * fee2 / 100) - (bid_price * fee1 / 100)
    profit_percent = (net_profit / ask_price) * 100

    return profit_percent


def main():
    it = 0
    while True:
        bybit_data = get_bybit_data(symbol)
        binance_data = get_binance_data(symbol)
        okx_data = get_okx_data(symbol='BTC-USDT')

        arbitrages = [
            ('bybit', 'binance', bybit_data, binance_data),
            ('binance', 'bybit', binance_data, bybit_data),
            ('okx', 'bybit', okx_data, bybit_data),
            ('okx', 'binance', okx_data, binance_data),
            ('bybit', 'okx', bybit_data, okx_data),
            ('binance', 'okx', binance_data, okx_data)
        ]

        for exchange1, exchange2, data1, data2 in arbitrages:
            profit_percent = arbitrage(exchange1, exchange2, data1, data2, it)
            if profit_percent > 0.5:
                print(f"### Arbitrage opportunity ### \nSell on {exchange1} \nBuy on {exchange2} \nPotential profit: {profit_percent:.2f}%")
        it += 1


if __name__ == "__main__":
    main()

'''
1. підключити функцію яка зчитує всі пари з біржі (bybit) і перевірити чи відрізняються комісії між парами
2. якщо відрізняються то треба подумати якщо ні то ставимо ліміт кидання запиту кожні 60 ітерацій (get fees)
'''