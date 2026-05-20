rom datetime import datetime


def get_active_session():

    hour = datetime.utcnow().hour

    if 6 <= hour < 10:
        return "LONDON OPEN"

    if 13 <= hour < 17:
        return "NEW YORK OPEN"

    return "ASIAN SESSION"
