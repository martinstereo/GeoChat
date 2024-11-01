import psycopg2
from config import DB_CONFIG

def retrieve_vectors(query_vector, limit=5):
    """Retrieve the most relevant vectors from the database."""
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Query to find the closest vectors (assuming you have some similarity measure)
    cursor.execute("""
        SELECT filename, vector
        FROM pdf_vectors
        ORDER BY vector <-> %s
        LIMIT %s
    """, (query_vector, limit))

    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
