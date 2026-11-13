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

def read_book_details():
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    category = input("Category: ").strip()

    year_text = input("Published Year: ").strip()

    try:
        published_year = int(year_text)
    except ValueError:
        raise ValueError("Published year must be an Integer")

    price_text = input("Price: ").strip()

    try:
        price = Decimal(price_text)
    except InvalidOperation:
        raise ValueError("Price must be a valid amount")

    return title, author, category, published_year, price


def display_book(book):

    print("-" * 35)
    print(f"ID: {book['book_id']}")
    print(f"Title: {book['title']}")
    print(f"Author: {book['author']}")
    print(f"Category: {book['category']}")
    print(f"Year: {book['published_year']}")
    print(f"Price: ${book['price']:.2f}")
    print("-" * 35)


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