from binance.client import Client
from binance.enums import *
from config import BaseConfig, BinanceConfig
from app.items import Ticker


class BinanceAction(object):

    def __init__(self):
        self.client = Client(BinanceConfig.api_key, BinanceConfig.api_secret, {'proxies': BaseConfig.proxies})
        self.markets = BinanceConfig.markets

    def get_asset(self, symbol):
        """
        Symbol to (quote_asset, base_asset)
        :param symbol:
        :return: (quote_asset, base_asset)
        """
        quote_asset = None
        base_asset = None
        for market in self.markets:
            if symbol.endswith(market):
                base_asset = market
                quote_asset = symbol[:len(symbol) - len(market)]
        return quote_asset, base_asset

    def get_market(self):
        """
        :return: tickers: [{"name":BTCUSDT,"base_asset":"USDT","quote_asset":"BTC","price":8422.64,"usdt_price":8422.64}]
        """
        tickers = []
        # Get the last price info in whitelist and turn into a dict
        tickers_raw = self.client.get_all_tickers()
        tickers_whitelist = {}
        if len(tickers_raw) > 0:
            for ticker in tickers_raw:
                if ticker["symbol"] in BinanceConfig.whitelist:
                    tickers_whitelist[ticker["symbol"]] = ticker["price"]
        # Get the last market price list
        usdt_prices = {}
        for market in self.markets:
            if market == "USDT":
                usdt_prices[market] = 1.0
            elif market + "USDT" in tickers_whitelist:
                usdt_prices[market] = float(tickers_whitelist[market + "USDT"])
        # Get the symbol list
        for ticker_white in tickers_whitelist:
            quote_asset, base_asset = self.get_asset(ticker_white)
            if quote_asset is None and base_asset is None:
                continue
            price = float(tickers_whitelist[ticker_white])
            usdt_price = price * float(usdt_prices[base_asset])
            ticker = Ticker(symbol=ticker_white, quote_asset=quote_asset, base_asset=base_asset, price=price,
                            usdt_price=usdt_price)
            tickers.append(ticker)
        return tickers

    def get_depth_price(self, symbol, side, quantity):
        """
        Compute the ave price according to quantity and price if I buy/sell
        :param symbol:
        :param side:
        :param quantity:
        :return:6371.1
        """
        depth = self.client.get_order_book(symbol=symbol)
        order_list = []
        if side == SIDE_BUY:
            order_list = depth["asks"]
        elif side == SIDE_SELL:
            order_list = depth["bids"]
        if len(order_list) > 0:
            ave_price = 0
            sum_quantity = 0
            sum_vol = 0
            for i in range(len(order_list)):
                order = order_list[i]
                sum_quantity = sum_quantity + float(order[1])
                sum_vol = sum_vol + float(order[1]) * float(order[0])
                if i < len(order_list):
                    if sum_quantity >= quantity:
                        depth_price = sum_vol / sum_quantity
                        break
            return depth_price

    def check_balance(self, symbol, side):
        """
        Check the balance of asset

        :param side:
        :type symbol
        :return: 1
        """
        balance = 0.0
        quote_asset, base_asset = self.get_asset(symbol)
        if side == SIDE_BUY:
            balance_json = self.client.get_asset_balance(asset=base_asset)
            balance = float(balance_json["free"])
        elif side == SIDE_SELL:
            balance_json = self.client.get_asset_balance(asset=quote_asset)
            balance = float(balance_json["free"])
        # Check the balance of asset
        if balance > 0.0:
            return balance

    def create_test_order(self, symbol, side, quantity):
        """
        Create a test MARKET Order
        :param symbol:
        :param side:
        :param quantity:
        """
        self.client.create_test_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)

    def create_order(self, symbol, side, quantity):
        """
        Create an MARKET Order
        :param symbol:
        :param side:
        :param quantity:
        """
        self.client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
