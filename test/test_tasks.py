from binance.enums import *

from app.action.binance_action import BinanceAction
from app.arbitrages import triangular_arbitrage
from config import BinanceConfig


def test_triangular_arbitrage_task():
    action = BinanceAction()
    tickers = action.get_market()
    arbitrages = triangular_arbitrage(tickers, "USDT", BinanceConfig.fee, 0.02)
    for arbitrage in arbitrages:
        # Check the arbitrage
        price = []
        for i in range(3):
            ticker = arbitrage[i]
            if i < 2:
                if action.get_price(ticker.symbol, SIDE_BUY) is not None:
                    price.append(action.get_price(ticker.symbol, SIDE_BUY))
                else:
                    continue
            elif i == 2:
                if action.get_price(ticker.symbol, SIDE_SELL) is not None:
                    price.append(action.get_price(ticker.symbol, SIDE_SELL))
                else:
                    continue
        p1 = float(price[0])
        p2 = float(price[1])
        p3 = float(price[2])
        fee = BinanceConfig.fee
        rate = 1 - p1 * (1 - fee) * (1 - fee) * (1 - fee) / (p2 * p3)
        print(rate)
