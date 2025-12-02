import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # agar parolingiz bo‘lsa yozing
            database="auto_rezyume",
            port=3306
        )
        return conn
    except Error as e:
        print("MySQL bilan ulanishda xato:", e)
        return None
