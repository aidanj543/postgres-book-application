import os
import psycopg
from dotenv import load_dotenv
from decimal import Decimal, InvalidOperation
from psycopg.rows import dict_row

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



def validate_book_id(book_id):
    if type(book_id) is not int or book_id <=0:
        raise ValueError("Book ID must be positive")

    return book_id


def validate_book_details(title, author, category, published_year, price):
    """Validate book details before inserting or updating."""

    text_fields = {
        "title": (title, 150),
        "author": (author, 100),
        "category": (category, 50),
    }

    cleaned = {}

    for name, (value, max_length) in text_fields.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} cannot be empty.")

        value = value.strip()

        if len(value) > max_length:
            raise ValueError(
                f"{name} cannot exceed {max_length} characters."
            )

        cleaned[name] = value

    if type(published_year) is not int or not (0 <= published_year <= 9999):
        raise ValueError("Published year must be an integer from 0 to 9999.")

    try:
        amount = Decimal(str(price))
    except (InvalidOperation, ValueError):
        raise ValueError("Price must be a valid number.")

    if not amount.is_finite() or amount < 0 or amount > Decimal("99999999.99"):
        raise ValueError("Price must be between 0 and 99999999.99.")

    if amount != amount.quantize(Decimal("0.01")):
        raise ValueError("Price cannot have more than two decimal places.")

    return (
        cleaned["title"],
        cleaned["author"],
        cleaned["category"],
        published_year,
        amount,
    )


def add_book(title, author, category, published_year, price):

    details = validate_book_details(title, author, category, published_year, price)

    query = """
        INSERT INTO books
            (title, author, category, published_year, price)
        VALUE(%s, %s, %s, %s, %s)
        RETURNING book_id
    """

    with get_connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, details)
            book_id = cursor.fetchone()[0]

    return book_id

def view_all_books():

    query = """
        SELECT book_id, title, author, category, published_year, price
        FROM books
        ORDER BY book_id;
    """

    with get_connection as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            books = cursor.fetchall()
    return books


def get_book_by_id(book_id):
    pass

def update_book(book_id, title, author, category, published_year, price):
    pass

def delete_book(book_id):
    pass

