from contextlib import contextmanager
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


DB_NAME: str = os.getenv('DB_NAME')
DB_USER: str = os.getenv('DB_USER')
DB_PASS: str = os.getenv('DB_PASS')
DB_HOST: str = os.getenv('DB_HOST')
DB_PORT: str = os.getenv('DB_PORT')

class Connection:
    connection = None

    def __init__(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT
            )

    @contextmanager
    def cursor(self, commit: bool = False):
        try:
            cursor = self.connection.cursor()
            yield cursor
        finally:
            if commit:
                self.commit()
            cursor.close()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
