import sqlite3
import datetime

from config import DB_PATH

def init_db():
    """Ініціалізація SQLite бази для збереження графіків"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            data TEXT NOT NULL,
            updated TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_schedule(date: str, data: str, updated: str):
    """Збереження нового графіка"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM schedules WHERE date=?', (date,)
    )
    cursor.execute(
        'INSERT INTO schedules (date, data, updated) VALUES (?, ?, ?)', 
        (date, data, updated)
    )
    conn.commit()
    conn.close()

def get_schedule(date: str):
    """Отримання графіка за датою"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT data, updated FROM schedules WHERE date=?', (date,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'data': row[0], 'updated': row[1]}
    return None

def get_last_schedule():
    """Отримання останнього збереженого графіка"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT date, data, updated FROM schedules ORDER BY updated DESC LIMIT 1'
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'date': row[0], 'data': row[1], 'updated': row[2]}
    return None

def schedules_equal(new: str, old: str):
    """Порівняння графіків на предмет змін"""
    return new.strip() == old.strip()