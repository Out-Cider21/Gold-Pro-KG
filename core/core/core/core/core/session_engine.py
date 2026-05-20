from datetime import datetime


def current_session():
    hour = datetime.utcnow().hour

    if 0 <= hour < 5:
        return "ASIAN RANGE"

    if 6 <= hour < 10:
        return "LONDON OPEN"

    if 10 <= hour < 12:
        return "LONDON MIDDAY"

    if 13 <= hour < 17:
        return "NEW YORK OPEN"

    if 17 <= hour < 20:
        return "LONDON CLOSE"

    return "OFF KILLZONE"


def quarterly_phase():
    now = datetime.utcnow()
    total_minutes = now.hour * 60 + now.minute

    quarter = total_minutes // 360 + 1

    phases = {
        1: "Q1 ACCUMULATION",
        2: "Q2 MANIPULATION",
        3: "Q3 DISTRIBUTION",
        4: "Q4 REVERSAL / REBALANCE",
    }

    return phases.get(quarter, "UNKNOWN")
