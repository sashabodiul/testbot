from data import config
import psycopg2
from datetime import datetime
import json 


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
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def add_currency_record(buy_data, sell_data):
    conn = conn_to_db()
    cursor = conn.cursor()

    created_at = datetime.now()

    # Преобразуем словари buy_data и sell_data в строки JSON
    buy_data_json = json.dumps(buy_data)
    sell_data_json = json.dumps(sell_data)

    cursor.execute(
        'INSERT INTO "Currency" (buy, sell, created_at) VALUES (%s, %s, %s)',
        (buy_data_json, sell_data_json, created_at)
    )

    conn.commit()
    cursor.close()
    close_db(conn)


def get_latest_currency_record():
    try:
        conn = conn_to_db()
        cursor = conn.cursor()

        query = "SELECT buy, sell, created_at FROM \"Currency\" ORDER BY created_at DESC LIMIT 1;"
        cursor.execute(query)
        
        latest_record = cursor.fetchone()
        cursor.close()
        close_db(conn)
        return latest_record
    except Exception as e:
        print(f"An error occurred: {e}")
        return None