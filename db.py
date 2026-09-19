import sqlite3
import datetime


def create_table():

    with sqlite3.connect("history.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_stamp TEXT,
            delay_ratio REAL,
            delay_minutes REAL,
            status TEXT
        )""")
        conn.commit()


def log_check(time_stamp, delay_ratio, delay_minutes, status):
    with sqlite3.connect("history.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO traffic_log (time_stamp, delay_ratio, delay_minutes, status)
        VALUES(?,?,?,?)
        """,
            (time_stamp, delay_ratio, delay_minutes, status),
        )
        conn.commit()
