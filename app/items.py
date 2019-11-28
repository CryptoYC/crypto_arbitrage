class Ticker(object):
    def __init__(self, symbol, base_asset, quote_asset, price, usdt_price):
        self.symbol = symbol
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.price = price
        self.usdt_price = usdt_price
