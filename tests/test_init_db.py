import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

import unittest
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_CONFIG
from init_db import init_database

class TestInitDB(unittest.TestCase):
    def setUp(self):
        print(f"\nRunning test: {self._testMethodName}")
        self.test_db_name = 'test_' + DB_CONFIG['dbname']

    def tearDown(self):
        # Clean up test database
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port']
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.test_db_name}")
            conn.close()
        except OperationalError as e:
            print(f"Cleanup error: {e}")
        print(f"✓ {self._testMethodName} completed successfully\n")

    def test_database_creation(self):
        try:
            init_database()

            # Verify database exists
            connection = psycopg2.connect(**DB_CONFIG)
            cursor = connection.cursor()

            # Check vector extension
            cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
            self.assertIsNotNone(cursor.fetchone(), "Vector extension not found")

            # Check table schema
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'document_vectors'
            """)
            columns = [row[0] for row in cursor.fetchall()]

            self.assertIn('id', columns, "Missing id column")
            self.assertIn('text', columns, "Missing text column")
            self.assertIn('metadata', columns, "Missing metadata column")
            self.assertIn('embedding', columns, "Missing embedding column")

            connection.close()

        except OperationalError as e:
            self.fail(f"Database initialization failed: {e}")

if __name__ == '__main__':
    unittest.main(verbosity=2)