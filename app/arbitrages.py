def triangular_arbitrage(tickers, target_asset, fee, target_rate):
    """
    The triangular arbitrage
    :param tickers:
    :param target_asset: USDT
    :param fee:
    :param target_rate: 0.05
    :return:[["BATUSDT","BATBTC","BTCUSDT"]]
    """

    arbitrages = []
    # 1.Divide market
    target_market_tickers = list(filter(lambda ticker: ticker.base_asset == target_asset, tickers))
    other_market_tickers = list(filter(lambda ticker: ticker.base_asset != target_asset, tickers))
    # 2. Assume first , second and third ticker
    # First_ticker : B/A , Second_ticker : B/C , Third_ticker : C/A
    # First Ticker
    for first_ticker in target_market_tickers:
        # Second Ticker
        for second_ticker in other_market_tickers:
            if first_ticker.quote_asset == second_ticker.quote_asset and first_ticker.usdt_price < second_ticker.usdt_price:
                # Third ticker
                third_ticker_symbol = second_ticker.base_asset + first_ticker.base_asset
                third_ticker = next((ticker for ticker in tickers if ticker.symbol == third_ticker_symbol), None)
                p1 = first_ticker.price
                p2 = second_ticker.price
                p3 = third_ticker.price
                # r=1-p1*(1 - fee) * (1 - fee) * (1 - fee) / (p2 * p3)
                rate = 1 - p1 * (1 - fee) * (1 - fee) * (1 - fee) / (p2 * p3)
                if rate > target_rate:
                    print("process : " + first_ticker.symbol + "->" + second_ticker.symbol + "->" + third_ticker.symbol + " @ " + rate)
                    arbitrages.append([first_ticker.symbol, second_ticker.symbol, third_ticker.symbol])
    return arbitrages
