import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect without database first
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS auto_rezyume 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_general_ci
        """)
        print("✓ Database 'auto_rezyume' created")
        
        # Use the database
        cursor.execute("USE auto_rezyume")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                password VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table 'users' created")
        
        # Create resumes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                full_name VARCHAR(150),
                profession VARCHAR(150),
                about TEXT,
                education TEXT,
                experience TEXT,
                skills TEXT,
                template_name VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("✓ Table 'resumes' created")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("\n✅ Database setup completed successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_database()
