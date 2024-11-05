import psycopg2
from config import DB_CONFIG

def init_database():
    # Connect to default postgres database first
    default_conn = None
    try:
        # Use DB_CONFIG values but override dbname to connect to postgres first
        postgres_config = DB_CONFIG.copy()
        postgres_config['dbname'] = 'postgres'

        default_conn = psycopg2.connect(**postgres_config)
        default_conn.autocommit = True
        cur = default_conn.cursor()

        # Create database if not exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_CONFIG['dbname']}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {DB_CONFIG['dbname']}")
            print(f"Created database: {DB_CONFIG['dbname']}")
    except psycopg2.Error as e:
        print(f"Connection error: {e}")
    finally:
        if default_conn:
            default_conn.close()

    # Connect to the new database and create table
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Create vector extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")

        # Create table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS document_vectors (
            id BIGSERIAL PRIMARY KEY,
            text TEXT,
            metadata JSONB,
            embedding VECTOR(384)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Initialized table: document_vectors")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    init_database()