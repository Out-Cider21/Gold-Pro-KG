import sqlite3
import pandas as pd

DB_FILE = "immaculate_gold_pro.db"


def init_database():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        asset TEXT,
        bias TEXT,
        setup TEXT,
        outcome TEXT,
        profit REAL
    )
    ''')
