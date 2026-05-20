def swing_points(df, left=3, right=3):
    highs = []
    lows = []

    for i in range(left, len(df) - right):
        window = df.iloc[i - left:i + right + 1]
        row = df.iloc[i]

        if row["high"] == window["high"].max():
            highs.append((i, row["time"], row["high"]))

        if row["low"] == window["low"].min():
            lows.append((i, row["time"], row["low"]))

    return highs, lows


def detect_bos_choch(df):
    highs, lows = swing_points(df)

    if len(highs) < 2 or len(lows) < 2:
        return {
            "bias": "NEUTRAL",
            "bos": False,
            "choch": False,
            "last_high": None,
            "last_low": None,
        }

    last_close = df["close"].iloc[-1]

    last_high = highs[-1][2]
    previous_high = highs[-2][2]

    last_low = lows[-1][2]
    previous_low = lows[-2][2]

    bullish_bos = last_close > last_high and last_high > previous_high
    bearish_bos = last_close < last_low and last_low < previous_low

    bullish_choch = last_close > last_high and last_low < previous_low
    bearish_choch = last_close < last_low and last_high > previous_high

    if bullish_bos:
        bias = "BULLISH"
    elif bearish_bos:
        bias = "BEARISH"
    elif bullish_choch:
        bias = "BULLISH CHOCH"
    elif bearish_choch:
        bias = "BEARISH CHOCH"
    else:
        bias = "NEUTRAL"

    return {
        "bias": bias,
        "bos": bullish_bos or bearish_bos,
        "choch": bullish_choch or bearish_choch,
        "last_high": last_high,
        "last_low": last_low,
    }


def detect_fvg(df):
    fvgs = []

    for i in range(2, len(df)):
        candle_1 = df.iloc[i - 2]
        candle_3 = df.iloc[i]

        bullish_fvg = candle_1["high"] < candle_3["low"]
        bearish_fvg = candle_1["low"] > candle_3["high"]

        if bullish_fvg:
            fvgs.append({
                "type": "BULLISH FVG",
                "low": candle_1["high"],
                "high": candle_3["low"],
                "time": candle_3["time"],
            })

        if bearish_fvg:
            fvgs.append({
                "type": "BEARISH FVG",
                "low": candle_3["high"],
                "high": candle_1["low"],
                "time": candle_3["time"],
            })

    return fvgs[-8:]


def detect_liquidity_sweep(df):
    if len(df) < 80:
        return "NO CLEAR SWEEP"

    recent = df.tail(40)
    prior = df.iloc[-80:-40]

    prior_high = prior["high"].max()
    prior_low = prior["low"].min()

    last = recent.iloc[-1]

    sweep_high = last["high"] > prior_high and last["close"] < prior_high
    sweep_low = last["low"] < prior_low and last["close"] > prior_low

    if sweep_high:
        return "BUY-SIDE LIQUIDITY SWEPT"

    if sweep_low:
        return "SELL-SIDE LIQUIDITY SWEPT"

    return "NO CLEAR SWEEP"


def premium_discount(df):
    range_high = df["high"].tail(120).max()
    range_low = df["low"].tail(120).min()
    equilibrium = (range_high + range_low) / 2
    price = df["close"].iloc[-1]

    if price > equilibrium:
        zone = "PREMIUM"
    elif price < equilibrium:
        zone = "DISCOUNT"
    else:
        zone = "EQUILIBRIUM"

    return {
        "range_high": range_high,
        "range_low": range_low,
        "equilibrium": equilibrium,
        "zone": zone,
    }


def detect_malaysian_snr(df, lookback=80):
    data = df.tail(lookback).copy()

    zones = []

    for i in range(2, len(data) - 2):
        candle = data.iloc[i]
        prev_candle = data.iloc[i - 1]
        next_candle = data.iloc[i + 1]

        body_low = min(candle["open"], candle["close"])
        body_high = max(candle["open"], candle["close"])

        candle_range = abs(candle["high"] - candle["low"])

        bullish_engulfing = (
            candle["close"] > candle["open"]
            and prev_candle["close"] < prev_candle["open"]
            and candle["close"] > prev_candle["open"]
            and candle["open"] < prev_candle["close"]
        )

        bearish_engulfing = (
            candle["close"] < candle["open"]
            and prev_candle["close"] > prev_candle["open"]
            and candle["open"] > prev_candle["close"]
            and candle["close"] < prev_candle["open"]
        )

        double_open_close = (
            abs(candle["open"] - prev_candle["close"])
            <= candle_range * 0.15
        )

        swing_low = (
            candle["low"] < prev_candle["low"]
            and candle["low"] < next_candle["low"]
        )

        swing_high = (
            candle["high"] > prev_candle["high"]
            and candle["high"] > next_candle["high"]
        )

        if bullish_engulfing or (swing_low and double_open_close):
            zones.append({
                "type": "SUPPORT",
                "low": body_low,
                "high": body_high,
                "time": candle["time"],
                "strength": 80 if bullish_engulfing else 65,
            })

        if bearish_engulfing or (swing_high and double_open_close):
            zones.append({
                "type": "RESISTANCE",
                "low": body_low,
                "high": body_high,
                "time": candle["time"],
                "strength": 80 if bearish_engulfing else 65,
            })

    return zones[-12:]
