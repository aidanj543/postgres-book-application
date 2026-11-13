from database import get_connection, add_book, search_book_by_id, update_book, delete_book, view_all_books
from decimal import Decimal, InvalidOperation
import psycopg



def read_positive_id():
    value = input("Enter book ID: ").strip()

    try:
        book_id = int(value)
    except ValueError:
        raise ValueError("Book ID must be an Integer")

    if book_id <= 0:
        raise ValueError("Book ID must be positive")

    return book_id



def main():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()

                print("Connected to PostgreSQL!!")
                print("Server Version: ", result[0])

    except (ConnectionError, ValueError) as e:
        print("Database connection failed: ", e)

    except Exception as e:
        print("Random error: ", type(e).__name__)


if __name__ == "__main__":
    main()