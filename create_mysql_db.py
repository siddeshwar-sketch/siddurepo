import pymysql

# Connection details
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'siddu@2005',
    'port': 3306,
}

try:
    # Connect to MySQL server (not a specific DB)
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    
    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS finalproject")
    print("Database 'finalproject' created successfully or already exists!")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error creating database: {e}")
