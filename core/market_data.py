import pandas as pd
import numpy as np
from datetime import datetime, timedelta

try:
    import MetaTrader5 as mt5
except Exception:
    mt5 = None


SYMBOL_MAP = {
    "XAUUSD": "XAUUSD",
    "BTCUSD": "BTCUSD",
    "EURUSD": "EURUSD",
    "US30": "US30",
    "NAS100": "NAS100",
}


def mt5_timeframes():
    if mt5 is None:
        return {}

    return {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }


def mt5_available():
    if mt5 is None:
        return False

    return mt5.initialize()


def get_mt5_rates(symbol, timeframe, bars=320):
    if not mt5_available():
        return None

    tf_map = mt5_timeframes()
    mt5_symbol = SYMBOL_MAP.get(symbol, symbol)
    tf = tf_map.get(timeframe)

    if tf is None:
        return None

    rates = mt5.copy_rates_from_pos(mt5_symbol, tf, 0, bars)

    if rates is None or len(rates) == 0:
        return None

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.rename(columns={"tick_volume": "volume"}, inplace=True)

    return df[["time", "open", "high", "low", "close", "volume"]]


def synthetic_rates(symbol, bars=320):
    base_price = {
        "XAUUSD": 4680.0,
        "BTCUSD": 108000.0,
        "EURUSD": 1.0845,
        "US30": 39250.0,
        "NAS100": 18900.0,
    }.get(symbol, 1000.0)

    volatility = {
        "XAUUSD": 4.5,
        "BTCUSD": 450.0,
        "EURUSD": 0.002,
        "US30": 80.0,
        "NAS100": 55.0,
    }.get(symbol, 5.0)

    rows = []
    price = base_price

    for i in range(bars):
        candle_time = datetime.now() - timedelta(minutes=bars - i)

        open_price = price
        close_price = open_price + np.random.normal(0, volatility)
        high_price = max(open_price, close_price) + abs(np.random.normal(0, volatility / 2))
        low_price = min(open_price, close_price) - abs(np.random.normal(0, volatility / 2))
        volume = np.random.randint(100, 2000)

        rows.append([
            candle_time,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
        ])

        price = close_price

    return pd.DataFrame(
        rows,
        columns=["time", "open", "high", "low", "close", "volume"]
    )


def get_market_data(symbol, timeframe, bars=320, live_mode=False):
    if live_mode:
        df = get_mt5_rates(symbol, timeframe, bars)

        if df is not None:
            return df, "MT5 LIVE"

    return synthetic_rates(symbol, bars), "SIMULATION"
