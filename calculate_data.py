from get_fee import get_binance_fee, get_bybit_fee, get_okx_fee


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


def arbitrage_okx_to_bybit(bybit_data, okx_data):
    okx_bid = okx_data['bid_price']
    bybit_ask = bybit_data['ask_price']

    fee_bybit, _ = get_bybit_fee()
    fee_okx, _ = get_okx_fee()

    # Calculate potential profit
    spread = okx_bid - bybit_ask
    net_profit = spread - (bybit_ask * fee_bybit / 100) - (okx_bid * fee_okx / 100)

    return net_profit


def arbitrage_okx_to_binance(binance_data, okx_data):
    okx_bid = okx_data['bid_price']
    binance_ask = binance_data['ask_price']

    fee_binance, _ = get_binance_fee()
    fee_okx, _ = get_okx_fee()

    # Calculate potential profit
    spread = okx_bid - binance_ask
    net_profit = spread - (binance_ask * fee_binance / 100) - (okx_bid * fee_okx / 100)

    return net_profit


def arbitrage_bybit_to_okx(bybit_data, okx_data):
    bybit_bid = bybit_data['bid_price']
    okx_ask = okx_data['ask_price']

    fee_bybit, _ = get_bybit_fee()
    fee_okx, _ = get_okx_fee()

    # Calculate potential profit
    spread = bybit_bid - okx_ask
    net_profit = spread - (okx_ask * fee_okx / 100) - (bybit_bid * fee_bybit / 100)

    return net_profit


def arbitrage_binance_to_okx(binance_data, okx_data):
    binance_bid = binance_data['bid_price']
    okx_ask = okx_data['ask_price']

    fee_binance, _ = get_binance_fee()
    fee_okx, _ = get_okx_fee()

    # Calculate potential profit
    spread = binance_bid - okx_ask
    net_profit = spread - (okx_ask * fee_okx / 100) - (binance_bid * fee_binance / 100)

    return net_profit
