# src/init_db.py
import psycopg2
from psycopg2 import Error
from config import DB_CONFIG

def init_database():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS pdf_vectors (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        vector FLOAT8[] NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        # Connect to database
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Create table
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'pdf_vectors' initialized successfully")

    except Error as e:
        print(f"Error initializing database: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    init_database()