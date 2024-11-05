import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

import unittest
from config import DB_CONFIG
import psycopg2
from psycopg2 import OperationalError

class TestDBConfig(unittest.TestCase):
    def setUp(self):
        print(f"\nRunning test: {self._testMethodName}")

    def tearDown(self):
        print(f"✓ {self._testMethodName} completed successfully\n")

    def test_db_connection(self):
        try:
            connection = psycopg2.connect(**DB_CONFIG)
            self.assertTrue(connection.closed == 0)
            connection.close()
            print("Successfully connected and closed database connection")
        except OperationalError as e:
            self.fail(f"Database connection failed: {e}")

    def test_db_config_keys(self):
        required_keys = {'dbname', 'user', 'password', 'host', 'port'}
        self.assertEqual(set(DB_CONFIG.keys()), required_keys)
        print(f"DB_CONFIG contains all required keys: {', '.join(required_keys)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)