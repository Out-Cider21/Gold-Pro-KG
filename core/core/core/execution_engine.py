try:
    import MetaTrader5 as mt5
except Exception:
    mt5 = None


EXECUTION_ENABLED = False


def mt5_available():
    if mt5 is None:
        return False

    return mt5.initialize()


def place_mt5_order(symbol, direction, lot, sl, tp):
    if not EXECUTION_ENABLED:
        return False, "Execution is disabled by default."

    if not mt5_available():
        return False, "MT5 unavailable."

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        return False, "No MT5 tick data."

    order_type = mt5.ORDER_TYPE_BUY if direction == "BUY" else mt5.ORDER_TYPE_SELL
    price = tick.ask if direction == "BUY" else tick.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 26052026,
        "comment": "Immaculate Gold Pro",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result is None:
        return False, "Order failed."

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        return True, "MT5 order sent successfully."

    return False, str(result)
