import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    required_vars = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]

    missing = [name for name in required_vars if not os.getenv(name)]

    if missing:
        raise ValueError(
            "Missing database config: " + ", ".join(missing)
        )

    try:
        connection = psycopg.connect(
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            connect_timeout=5
        )

        return connection

    except psycopg.OperationalError as e:
        raise ConnectionError(
            "Unable to connect to database"
        ) from e