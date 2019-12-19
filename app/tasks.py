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
    arbitrages = triangular_arbitrage(tickers, BinanceConfig.fee, 0.01)
    for arbitrage in arbitrages:
        print("Start of arbitrage :" + arbitrage)
        process = arbitrage["process"]
        for symbol in process:
            # Get the quantity
            quantity = action.check_balance(symbol, SIDE_BUY)
            # Create the order
            response = action.create_test_order(symbol, SIDE_BUY, quantity)
            if response is not None:
                print("Success in trade : " + symbol)
        print("End of arbitrage :" + arbitrage)
