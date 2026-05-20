def calculate_lot_size(symbol, risk_amount, stop_loss_distance):

    if stop_loss_distance <= 0:
        return 0, 0

    pip_values = {
        "XAUUSD": 1.0,
        "EURUSD": 10.0,
        "BTCUSD": 1.0,
        "US30": 1.0,
        "NAS100": 1.0
    }

    pip_value = pip_values.get(symbol, 1.0)

    lot_size = risk_amount / (stop_loss_distance * pip_value)
  
    exposure = lot_size * stop_loss_distance

    return round(lot_size, 2), round(exposure, 2)
