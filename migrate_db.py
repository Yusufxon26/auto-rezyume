import mysql.connector
from mysql.connector import Error

def add_photo_column():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        cursor.execute("USE auto_rezyume")
        
        # Check if photo_path column already exists
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='resumes' AND COLUMN_NAME='photo_path'
        """)
        
        if cursor.fetchone() is None:
            cursor.execute("""
                ALTER TABLE resumes 
                ADD COLUMN photo_path VARCHAR(255) DEFAULT NULL
            """)
            print("✓ Column 'photo_path' added to 'resumes' table")
        else:
            print("✓ Column 'photo_path' already exists")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Migration completed!")
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_photo_column()
