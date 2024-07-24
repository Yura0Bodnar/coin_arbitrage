from get_fee import get_okx_fee, get_binance_fee, get_bybit_fee
from fetch_pairs import association_pairs
from get_data import *
import time


# feee_bybit = {'DGBUSDT': 0.0018, 'ARBUSDT': 0.0018, 'AEVOUSDT': 0.0018, 'TNSRUSDT': 0.0018, 'EGLDUSDT': 0.0018, 'GRTUSDT': 0.0018, 'CELOUSDT': 0.0018, 'WBTCUSDT': 0.0018, 'RPLUSDT': 0.0018, 'LINKUSDT': 0.0018, 'SHIBUSDT': 0.0018, 'BICOUSDT': 0.0018, 'XLMUSDT': 0.0018, 'FILUSDT': 0.0018, 'NOTUSDT': 0.0018, 'YFIUSDT': 0.0018, 'AAVEUSDT': 0.0018, 'KDAUSDT': 0.0018, 'CRVUSDT': 0.0018, 'JTOUSDT': 0.0018, 'MAGICUSDT': 0.0018, 'MATICUSDT': 0.0018, 'SOLUSDT': 0.0018, 'WLDUSDT': 0.0018, 'GMXUSDT': 0.0018, 'USDCUSDT': 0.0, 'RENUSDT': 0.0018, 'IMXUSDT': 0.0018, 'SNXUSDT': 0.0018, 'WAXPUSDT': 0.0018, 'DCRUSDT': 0.0018, 'ZROUSDT': 0.0018, 'APTUSDT': 0.0018, 'TUSDT': 0.0018, 'OPUSDT': 0.0018, 'AXSUSDT': 0.0018, 'ADAUSDT': 0.0018, 'TIAUSDT': 0.0018, 'PERPUSDT': 0.0018, 'MOVRUSDT': 0.0018, 'FETUSDT': 0.0018, 'GLMRUSDT': 0.0018, 'SSVUSDT': 0.0018, 'FLOWUSDT': 0.0018, 'DOTUSDT': 0.0018, 'INJUSDT': 0.0018, 'ENSUSDT': 0.0018, 'ORDIUSDT': 0.0018, 'BCHUSDT': 0.0018, 'UNIUSDT': 0.0018, 'ZRXUSDT': 0.0018, 'WUSDT': 0.0018, 'ETHUSDT': 0.0018, 'FXSUSDT': 0.0018, 'CITYUSDT': 0.0018, 'LUNAUSDT': 0.0018, 'MASKUSDT': 0.0018, 'XTZUSDT': 0.0018, 'DYDXUSDT': 0.0018, 'WOOUSDT': 0.0018, 'RDNTUSDT': 0.0018, 'BNTUSDT': 0.0018, 'CHZUSDT': 0.0018, 'ARUSDT': 0.0018, 'JUPUSDT': 0.0018, 'UMAUSDT': 0.0018, 'SUIUSDT': 0.0018, 'BONKUSDT': 0.0018, 'ACAUSDT': 0.0018, 'LDOUSDT': 0.0018, 'TRXUSDT': 0.0018, 'ALGOUSDT': 0.0018, 'NEARUSDT': 0.0018, 'BATUSDT': 0.0018, 'EOSUSDT': 0.0018 ,'ZKUSDT': 0.0018, 'FTMUSDT': 0.0018, 'PYTHUSDT': 0.0018, 'AGLDUSDT': 0.0018, 'ACHUSDT': 0.0018, 'BLURUSDT': 0.0018, 'ICPUSDT': 0.0018, 'LTCUSDT': 0.0018, 'AVAXUSDT': 0.0018, 'DOGEUSDT': 0.0018, 'MKRUSDT': 0.0018, 'JSTUSDT': 0.0018, 'THETAUSDT': 0.0018, 'USTCUSDT': 0.0018, 'GALAUSDT': 0.0018, 'SCUSDT': 0.0018, 'BNBUSDT': 0.0018, 'SPELLUSDT': 0.0018, 'LUNCUSDT': 0.0018, 'GMTUSDT': 0.0018, 'MINAUSDT': 0.0018, 'SUSHIUSDT': 0.0018, 'ATOMUSDT': 0.0018, 'SLPUSDT': 0.0018, 'COMPUSDT': 0.0018, 'ONEUSDT': 0.0018, 'STRKUSDT': 0.0018, 'ICXUSDT': 0.0018, 'PEPEUSDT': 0.0018, 'SANDUSDT': 0.0018, 'ETCUSDT': 0.0018, 'ETHFIUSDT': 0.0018, 'MANAUSDT': 0.0018, 'QTUMUSDT': 0.0018, 'BTCUSDT': 0.0018, 'STXUSDT': 0.0018, 'APEUSDT': 0.0018, 'RVNUSDT': 0.0018, 'IDUSDT': 0.0018, 'HBARUSDT': 0.0018, 'ZILUSDT': 0.0018, 'MEMEUSDT': 0.0018, 'LRCUSDT': 0.0018, 'XRPUSDT': 0.0018, 'PEOPLEUSDT': 0.0018, 'WIFUSDT': 0.0018, '1INCHUSDT': 0.0018, 'FLOKIUSDT': 0.0018, 'ENJUSDT': 0.0018, 'KSMUSDT': 0.0018, 'KLAYUSDT': 0.0018}
# feee_binance = {'ETCUSDT': 0.001, 'GLMRUSDT': 0.001, 'WOOUSDT': 0.001, 'KLAYUSDT': 0.001, 'ICPUSDT': 0.001, 'QTUMUSDT': 0.001, 'ICXUSDT': 0.001, 'XTZUSDT': 0.001, 'NOTUSDT': 0.001, 'AEVOUSDT': 0.001, 'CELOUSDT': 0.001, 'BCHUSDT': 0.001, 'RDNTUSDT': 0.001, 'SUIUSDT': 0.001, 'ORDIUSDT': 0.001, 'JUPUSDT': 0.001, 'ENSUSDT': 0.001, 'SUSHIUSDT': 0.001, 'GRTUSDT': 0.001, 'USTCUSDT': 0.001, 'COMPUSDT': 0.001, 'ZRXUSDT': 0.001, 'XLMUSDT': 0.001, 'NEARUSDT': 0.001, 'MEMEUSDT': 0.001, 'TIAUSDT': 0.001, 'AVAXUSDT': 0.001, 'MOVRUSDT': 0.001, 'USDCUSDT': 0.0, 'CITYUSDT': 0.001, 'WIFUSDT': 0.001, 'WUSDT': 0.001, 'LUNCUSDT': 0.001, 'ETHFIUSDT': 0.001, 'ACAUSDT': 0.001, 'AAVEUSDT': 0.001, 'RPLUSDT': 0.001, 'APEUSDT': 0.001, 'EOSUSDT': 0.001, 'ARBUSDT': 0.001, 'SOLUSDT': 0.001, 'FLOWUSDT': 0.001, 'KDAUSDT': 0.001, 'HBARUSDT': 0.001, 'SLPUSDT': 0.001, 'GMXUSDT': 0.001, 'LDOUSDT': 0.001, 'ADAUSDT': 0.001, 'PERPUSDT': 0.001, 'SSVUSDT': 0.001, 'BNTUSDT': 0.001, 'SNXUSDT': 0.001, 'ACHUSDT': 0.001, 'DYDXUSDT': 0.001, 'OPUSDT': 0.001, 'MATICUSDT': 0.001, 'PEOPLEUSDT': 0.001, 'BICOUSDT': 0.001, 'FLOKIUSDT': 0.001, 'TNSRUSDT': 0.001, 'BATUSDT': 0.001, 'SCUSDT': 0.001, 'CRVUSDT': 0.001, 'IDUSDT': 0.001, 'MAGICUSDT': 0.001, 'IMXUSDT': 0.001, 'XRPUSDT': 0.001, 'ARUSDT': 0.001, 'STRKUSDT': 0.001, 'STXUSDT': 0.001, 'ENJUSDT': 0.001, 'GMTUSDT': 0.001, 'UMAUSDT': 0.001, 'LTCUSDT': 0.001, 'INJUSDT': 0.001, 'WBTCUSDT': 0.001, 'ATOMUSDT': 0.001, 'PYTHUSDT': 0.001, 'AXSUSDT': 0.001, 'MASKUSDT': 0.001, 'YFIUSDT': 0.001, 'LINKUSDT': 0.001, 'ZROUSDT': 0.001, 'WAXPUSDT': 0.001, 'DOTUSDT': 0.001, 'LRCUSDT': 0.001, 'ALGOUSDT': 0.001, '1INCHUSDT': 0.001, 'RVNUSDT': 0.001, 'DOGEUSDT': 0.001, 'SHIBUSDT': 0.001, 'APTUSDT': 0.001, 'BONKUSDT': 0.001, 'GALAUSDT': 0.001, 'ETHUSDT': 0.001, 'ONEUSDT': 0.001, 'LUNAUSDT': 0.001, 'BLURUSDT': 0.001, 'CHZUSDT': 0.001, 'RENUSDT': 0.001, 'WLDUSDT': 0.001, 'MKRUSDT': 0.001, 'TRXUSDT': 0.001, 'FXSUSDT': 0.001, 'BNBUSDT': 0.001, 'SANDUSDT': 0.001, 'BTCUSDT': 0.001, 'EGLDUSDT': 0.001, 'ZKUSDT': 0.001, 'MANAUSDT': 0.001, 'UNIUSDT': 0.001, 'DGBUSDT': 0.001, 'PEPEUSDT': 0.001, 'JTOUSDT': 0.001, 'JSTUSDT': 0.001, 'FILUSDT': 0.001, 'ZILUSDT': 0.001, 'THETAUSDT': 0.001, 'FTMUSDT': 0.001, 'AGLDUSDT': 0.001, 'MINAUSDT': 0.001, 'KSMUSDT': 0.001, 'FETUSDT': 0.001, 'TUSDT': 0.001}
# feee_okx = {'MINA-USDT': 0.001, 'GMT-USDT': 0.001, 'NOT-USDT': 0.001, 'SC-USDT': 0.001, 'ONE-USDT': 0.001, 'GLMR-USDT': 0.001, 'FET-USDT': 0.001, 'DGB-USDT': 0.001, 'AEVO-USDT': 0.001, 'LUNA-USDT': 0.001, 'WIF-USDT': 0.001, 'AVAX-USDT': 0.001, 'AAVE-USDT': 0.001, 'BNB-USDT': 0.001, 'GRT-USDT': 0.001, 'STX-USDT': 0.001, 'ICP-USDT': 0.001, 'AR-USDT': 0.001, 'AXS-USDT': 0.001, 'KSM-USDT': 0.001, 'SOL-USDT': 0.001, 'PEPE-USDT': 0.001, 'COMP-USDT': 0.001, 'W-USDT': 0.001, 'SUI-USDT': 0.001, 'KDA-USDT': 0.001, 'LINK-USDT': 0.001, 'GALA-USDT': 0.001, 'MASK-USDT': 0.001, 'ADA-USDT': 0.001, 'FTM-USDT': 0.001, 'LTC-USDT': 0.001, 'MOVR-USDT': 0.001, 'ETH-USDT': 0.001, 'JST-USDT': 0.001, 'QTUM-USDT': 0.001, '1INCH-USDT': 0.001, 'ETHFI-USDT': 0.001, 'FXS-USDT': 0.001, 'YFI-USDT': 0.001, 'MEME-USDT': 0.001, 'TIA-USDT': 0.001, 'REN-USDT': 0.001, 'DOT-USDT': 0.001, 'IMX-USDT': 0.001, 'BLUR-USDT': 0.001, 'TNSR-USDT': 0.001, 'JTO-USDT': 0.001, 'ICX-USDT': 0.001, 'FIL-USDT': 0.001, 'MKR-USDT': 0.001, 'ENS-USDT': 0.001, 'WOO-USDT': 0.001, 'LDO-USDT': 0.001, 'ETC-USDT': 0.001, 'PEOPLE-USDT': 0.001, 'INJ-USDT': 0.001, 'STRK-USDT': 0.001, 'USDC-USDT': 0.001, 'ZIL-USDT': 0.001, 'APE-USDT': 0.001, 'XTZ-USDT': 0.001, 'BICO-USDT': 0.001, 'EGLD-USDT': 0.001, 'LUNC-USDT': 0.001, 'UMA-USDT': 0.001, 'USTC-USDT': 0.001, 'ATOM-USDT': 0.001, 'KLAY-USDT': 0.001, 'SLP-USDT': 0.001, 'ALGO-USDT': 0.001, 'CRV-USDT': 0.001, 'ID-USDT': 0.001, 'ACA-USDT': 0.001, 'JUP-USDT': 0.001, 'RDNT-USDT': 0.001, 'MANA-USDT': 0.001, 'SSV-USDT': 0.001, 'CITY-USDT': 0.001, 'SAND-USDT': 0.001, 'MATIC-USDT': 0.001, 'MAGIC-USDT': 0.001, 'EOS-USDT': 0.001, 'FLOW-USDT': 0.001, 'WBTC-USDT': 0.001, 'T-USDT': 0.001, 'BTC-USDT': 0.001, 'ARB-USDT': 0.001, 'ENJ-USDT': 0.001, 'GMX-USDT': 0.001, 'FLOKI-USDT': 0.001, 'TRX-USDT': 0.001, 'NEAR-USDT': 0.001, 'ORDI-USDT': 0.001, 'OP-USDT': 0.001, 'ZRX-USDT': 0.001, 'DOGE-USDT': 0.001, 'ACH-USDT': 0.001, 'APT-USDT': 0.001, 'HBAR-USDT': 0.001, 'WLD-USDT': 0.001, 'CHZ-USDT': 0.001, 'RPL-USDT': 0.001, 'PERP-USDT': 0.001, 'ZRO-USDT': 0.001, 'XLM-USDT': 0.001, 'SHIB-USDT': 0.001, 'BONK-USDT': 0.001, 'UNI-USDT': 0.001, 'BNT-USDT': 0.001, 'XRP-USDT': 0.001, 'PYTH-USDT': 0.001, 'DYDX-USDT': 0.001, 'WAXP-USDT': 0.001, 'BAT-USDT': 0.001, 'RVN-USDT': 0.001, 'LRC-USDT': 0.001, 'SUSHI-USDT': 0.001, 'ZK-USDT': 0.001, 'THETA-USDT': 0.001, 'BCH-USDT': 0.001, 'AGLD-USDT': 0.001, 'SNX-USDT': 0.001, 'CELO-USDT': 0.001}


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

    fee1 = get_fees(exchange1, symbol, symbol_okx)
    fee2 = get_fees(exchange2, symbol, symbol_okx)

    # Calculate potential profit
    spread = bid_price - ask_price
    net_profit = spread - (ask_price * fee2 / 100) - (bid_price * fee1 / 100)
    profit_percent = (net_profit / ask_price) * 100

    return profit_percent


def arbitrage_check(data1, data2):
    bid_price = data1['bid_price']
    ask_price = data2['ask_price']

    # Calculate potential profit
    spread = bid_price - ask_price
    profit_percent = (spread / ask_price) * 100

    return profit_percent


def add_hyphen(symbol):
    return f"{symbol[:-4]}-{symbol[-4:]}"


def main():
    it = 0
    pairs_okx, pairs = None, None
    while True:
        try:
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
                        profit_percent_check = arbitrage_check(data1, data2)
                        if profit_percent_check > 0.005:
                            profit_percent = arbitrage(exchange1, exchange2, data1, data2, pair, okx_pair)
                            print(f"### Arbitrage opportunity {pair} ### \nSell on {exchange1} \nBuy on {exchange2} \nPotential profit: {profit_percent:.2f}%")

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
