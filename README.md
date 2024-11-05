# GeoChat

## Database Setup
1. Make sure PostgreSQL is running on your system
2. Update database parameters in `src/config.py`:
   ```python
   DB_CONFIG = {
       'dbname': 'geo_chat',
       'user': 'your_username',
       'password': 'your_password',
       'host': 'localhost',
       'port': '5432'
   }
2. Initialize the database:
  ```bash
  python [init_db.py](http://_vscodecontentref_/1)
  ```
## Tests
  To run all tests:
  ```bash
  python -m unittest discover -s tests
  ```