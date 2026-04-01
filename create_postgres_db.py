import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connection details for PostgreSQL server
config = {
    'dbname': 'postgres', # Connect to default 'postgres' DB first
    'user': 'postgres',
    'password': 'siddu@2005',
    'host': 'localhost',
    'port': '5432',
}

try:
    # Connect to PostgreSQL server
    conn = psycopg2.connect(**config)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'siddudatabase'")
    exists = cursor.fetchone()
    
    if not exists:
        # Create database
        cursor.execute("CREATE DATABASE siddudatabase")
        print("Database 'siddudatabase' created successfully!")
    else:
        print("Database 'siddudatabase' already exists.")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error creating database: {e}")
    print("\nTip: Make sure your PostgreSQL server is running on port 5432.")
