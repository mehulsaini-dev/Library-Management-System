import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    try:
        conn = psycopg.connect(
        host = "localhost",
        dbname = "library_db",
        user = "postgres",
        password = os.getenv("DB_PASSWORD"),
        port = "5432"
        )

        print("Database Connected Successfully!")
        return conn

    except Exception as e:
        print("Database Connection Failed:",e)
        return None
