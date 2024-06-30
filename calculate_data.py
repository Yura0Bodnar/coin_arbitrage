from get_fee import get_binance_fee, get_bybit_fee


def arbitrage_bybit_to_binance(bybit_data, binance_data):
    bybit_bid = bybit_data['bid_price']
    binance_ask = binance_data['ask_price']

    fee_bybit, _ = get_bybit_fee()
    fee_bin, _ = get_binance_fee()

    # Calculate potential profit
    spread = bybit_bid - binance_ask
    net_profit = spread - (binance_ask * fee_bin / 100) - (bybit_bid * fee_bybit / 100)

    return net_profit


def arbitrage_binance_to_bybit(bybit_data, binance_data):
    bybit_ask = bybit_data['ask_price']
    binance_bid = binance_data['bid_price']

    fee_bybit, _ = get_bybit_fee()
    fee_bin, _ = get_binance_fee()

    # Calculate potential profit
    spread = binance_bid - bybit_ask
    net_profit = spread - (bybit_ask * fee_bin / 100) - (binance_bid * fee_bybit / 100)

    return net_profit
