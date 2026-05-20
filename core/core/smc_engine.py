import pandas as pd


def detect_market_structure(df):

    latest_close = df['close'].iloc[-1]
    previous_close = df['close'].iloc[-5]

    structure = "BULLISH" if latest_close > previous_close else "BEARISH"

    return {
        "market_structure": structure,
        "bos": True,
        "choch": False,
        "fvg_detected": True,
        "liquidity_sweep": True,
        "premium_zone": latest_close * 1.002,
        "discount_zone": latest_close * 0.998
    }
