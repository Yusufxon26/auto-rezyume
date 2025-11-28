import os
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        # Agar Render/hosting ENV bo'lsa — shuni ishlatadi
        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "")
        db_name = os.getenv("DB_NAME", "auto_rezyume")
        db_port = int(os.getenv("DB_PORT", 3306))

        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        return connection

    except Error as e:
        print("MySQL bilan ulanishda xato:", e)
        return None
