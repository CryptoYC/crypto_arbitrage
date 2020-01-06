from app.action.binance_action import BinanceAction
from app.arbitrages import triangular_arbitrage
from binance.enums import *
from config import BinanceConfig
from . import scheduler


@scheduler.task('interval', id='get_repositories_topic_task', seconds=30)
def triangular_arbitrage_task():
    """
    The task of triangular arbitrage
    :return:
    """
    # Get the arbitrages
    action = BinanceAction()
    tickers = action.get_market()
    # [["BATUSDT","BATBTC","BTCUSDT"]]
    arbitrages = triangular_arbitrage(tickers, BinanceConfig.fee, 0.01, 0.05)
    for arbitrage in arbitrages:
        print("Start of arbitrage :" + arbitrage)
        # Check the arbitrage
        for i in range(2):
            ticker = arbitrage[i]
            if i < 2:
                price = action.get_price(ticker.symbol, SIDE_BUY)
                usdt_price = ticker.usdt_price * (price / ticker.price)
                arbitrage[i].price = price
                arbitrage[i].usdt_price = usdt_price
            elif i == 2:
                price = action.get_price(ticker.symbol, SIDE_SELL)
                usdt_price = ticker.usdt_price * (price / ticker.price)
                arbitrage[i].price = price
                arbitrage[i].usdt_price = usdt_price
        if len(triangular_arbitrage(arbitrage, BinanceConfig.fee, 0.01, 0.05)) == 1:
            # Create the orders
            for i in range(2):
                symbol = arbitrage[i].symbol
                if i < 2:
                    quantity = action.check_balance(symbol, SIDE_BUY)
                    action.create_test_order(symbol, SIDE_BUY, quantity)
                elif i == 2:
                    quantity = action.check_balance(symbol, SIDE_SELL)
                    action.create_test_order(arbitrage[i], SIDE_SELL, quantity)
        print("End of arbitrage :" + arbitrage)
