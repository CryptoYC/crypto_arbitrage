from app.action.binance_action import BinanceAction
from app.arbitrages import triangular_arbitrage


def test_triangular_arbitrage():
    action = BinanceAction()
    tickers = action.get_market()
    print(triangular_arbitrage(tickers, "USDT", 0.001, 0.02))
