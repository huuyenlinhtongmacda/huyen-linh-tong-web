import sqlite3

DB_NAME = "users.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        TenTaiKhoan TEXT UNIQUE,
        MatKhau TEXT,
        Phone TEXT
    )
    """)

    conn.commit()
    conn.close()