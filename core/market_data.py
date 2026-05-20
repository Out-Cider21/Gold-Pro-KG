import pandas as pd
import numpy as np
from datetime import datetime


def get_live_price_data(symbol):

    # PLACEHOLDER
    # Replace with:
    # MetaTrader5
    # Binance Websocket
    # TradingView Feed

    rows = []

    base_price = {
        "XAUUSD": 4680,
        "BTCUSD": 108000,
        "EURUSD": 1.08,
        "US30": 39200,
        "NAS100": 18900
    }

    price = base_price[symbol]

    for i in range(100):

      open_price = price + np.random.uniform(-3, 3)
        close_price = open_price + np.random.uniform(-2, 2)
        high_price = max(open_price, close_price) + np.random.uniform(0, 2)
        low_price = min(open_price, close_price) - np.random.uniform(0, 2)

        rows.append({
            "time": datetime.now(),
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": np.random.randint(100, 1000)
        })

    return pd.DataFrame(rows)
