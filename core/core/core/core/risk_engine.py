from datetime import datetime


def calculate_lot_size(symbol, risk_amount, stop_distance):
    if stop_distance <= 0:
        return 0.0

    pip_values = {
        "XAUUSD": 1.0,
        "EURUSD": 10.0,
        "BTCUSD": 1.0,
        "US30": 1.0,
        "NAS100": 1.0,
    }

    pip_value = pip_values.get(symbol, 1.0)

    lot_size = risk_amount / (stop_distance * pip_value)

    return round(lot_size, 2)


def risk_lockout(trades, max_daily_loss, max_consecutive_losses):
    if trades.empty:
        return False, "Risk status clear"

    today = datetime.now().strftime("%Y-%m-%d")

    trades_today = trades[
        trades["timestamp"].astype(str).str.startswith(today)
    ]

    daily_pnl = trades_today["profit"].sum() if not trades_today.empty else 0

    if daily_pnl <= -abs(max_daily_loss):
        return True, "Maximum daily loss breached"

    recent_trades = trades.head(max_consecutive_losses)

    if len(recent_trades) >= max_consecutive_losses:
        if all(recent_trades["profit"] < 0):
            return True, "Consecutive loss lockout active"

    return False, "Risk status clear"
