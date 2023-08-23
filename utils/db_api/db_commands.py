from data import config
import psycopg2
from datetime import datetime


def conn_to_db():
    return psycopg2.connect(
        host=config.DBHOST,
        dbname=config.DATABASE,
        user=config.PGUSER,
        password=config.PGPASSWORD,
        port=5432
    )


def close_db(conn):
    conn.close()
    

def add_user(telegram_id, username, first_name, last_name, phone):
    conn = conn_to_db()
    cursor = conn.cursor()
    created_at = datetime.now()  # Текущее время
    cursor.execute(
        'INSERT INTO "User" (telegram_id, username, first_name, last_name, phone, created_at) VALUES (%s, %s, %s, %s, %s, %s)',
        (telegram_id, username, first_name, last_name, phone, created_at)
    )
    conn.commit()
    cursor.close()
    close_db(conn)

def user_exists(telegram_id):
    conn = conn_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM \"User\" WHERE telegram_id = %s", (telegram_id,))
    result = cursor.fetchone()
    cursor.close()
    close_db(conn)
    return result is not None

def select_users():
    try:
        conn = conn_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT telegram_id FROM \"User\"")
        result = cursor.fetchall()
        cursor.close()
        close_db(conn)
        return len(result) > 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
