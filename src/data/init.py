"""Инициализация БД SQLite"""

import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

conn: Connection | None = None
curs: Cursor | None = None

def get_db(name: str | None = None, reset: bool= False):
    """Подключение к файлу БД SqLite"""
    global conn, curs
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        name = os.getenv("INVENTORY_SQL_DB")    #пременная для подключения к БД
        top_dir = Path(__file__).resolve().parents[1]
        db_dir = top_dir / "db"
        db_name = "inventory.db"
        db_path = str(db_dir / db_name)
        name = os.getenv("INVENTORY_SQL_DB", db_path)
        # print("Путь к базе данных:", name)
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()
    
get_db()