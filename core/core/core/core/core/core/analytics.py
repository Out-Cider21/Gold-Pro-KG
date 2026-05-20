import pandas as pd


def calculate_analytics(df):

    if df.empty:
        return {}

    total_trades = len(df)

    wins = len(df[df['outcome'] == 'TP HIT'])

    win_rate = (wins / total_trades) * 100

    total_profit = df['profit'].sum()

    max_drawdown = df['profit'].min()

    expectancy = total_profit / total_trades

    return {
        "win_rate": round(win_rate, 2),
        "total_profit": round(total_profit, 2),
        "max_drawdown": round(max_drawdown, 2),
        "expectancy": round(expectancy, 2)
    }
