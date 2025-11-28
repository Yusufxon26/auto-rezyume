import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='auto_rezyume',
            user='root',
            password=''  # o'zingizning MySQL parolingiz
        )
        return connection
    except Error as e:
        print("MySQL bilan ulanishda xato:", e)
        return None
