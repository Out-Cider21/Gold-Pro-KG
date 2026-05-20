import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "immaculate_gold_pro.db"


def init_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            asset TEXT,
            session TEXT,
            quarterly_phase TEXT,
            bias TEXT,
            setup TEXT,
            confluence_score INTEGER,
            entry REAL,
            stop_loss REAL,
            take_profit REAL,
            risk_amount REAL,
            outcome TEXT,
            profit REAL,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_trade(
    asset,
    session,
    quarterly_phase,
    bias,
    setup,
    confluence_score,
    entry,
    stop_loss,
    take_profit,
    risk_amount,
    outcome,
    profit,
    notes,
):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trades (
            timestamp, asset, session, quarterly_phase, bias, setup,
            confluence_score, entry, stop_loss, take_profit,
            risk_amount, outcome, profit, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        asset,
        session,
        quarterly_phase,
        bias,
        setup,
        confluence_score,
        entry,
        stop_loss,
        take_profit,
        risk_amount,
        outcome,
        profit,
        notes,
    ))

    conn.commit()
    conn.close()


def get_trades():
    conn = sqlite3.connect(DB_FILE)

    try:
        df = pd.read_sql_query("SELECT * FROM trades ORDER BY id DESC", conn)
    except Exception:
        df = pd.DataFrame()

    conn.close()
    return df


def clear_trades():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM trades")
    conn.commit()
    conn.close()
