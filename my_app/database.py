import sqlite3
from sqlite3 import Connection

def get_db_connection() -> Connection:
    """
    Создает и возвращает соединение с базой данных SQLite.
    """
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row
    return conn
