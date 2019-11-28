from unittest import TestCase
from app.action.binance_action import BinanceAction
from binance.enums import *


class TestBinanceAction(TestCase):
    def test_get_asset(self):
        action = BinanceAction()
        print(action.get_asset("BTCUSDT"))

    def test_get_market(self):
        action = BinanceAction()
        print(action.get_market())

    def test_create_order(self):
        action = BinanceAction()
        print(action.create_order("BTCUSDT", SIDE_BUY, 1))

    def test_create_test_order(self):
        action = BinanceAction()
        print(action.create_test_order("BNBBTC", SIDE_BUY, 1))

    def test_check_balance(self):
        action = BinanceAction()
        print(action.check_balance("BTCUSDT", SIDE_SELL))
