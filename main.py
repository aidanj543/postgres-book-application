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



def help_add_book():
    print("\n--- Add new book ---")
    details = read_book_details()
    book_id = add_book(*details)

    print(f"\nBook added! Book ID: {book_id}")



def help_view_all_books():
    print("\n--- All Current Books ---")

    books = view_all_books()

    if not books:
        print("No books found in database")

    print(f"Total books: {len(books)}")

    for book in books:
        display_book(book)



def help_search_book():
    print("\n--- Searching for Book ---")

    book_id = read_positive_id()

    book = search_book_by_id(book_id)

    if book is None:
        print(f"Book was not found with ID: {book_id}")
    else:
        display_book(book)



def help_update_book():

    print("\n--- Update a Book ---")

    book_id = read_positive_id()

    existing_book = search_book_by_id(book_id)

    if existing_book is None:
        print(f"Book was not found with ID: {book_id}")
        return

    print("\nCurrent book details:")
    display_book(existing_book)

    print("\nEnter the updated details:")
    details = read_book_details()

    updated = update_book(book_id, *details)

    if updated:
        print("\nBook updated successfully!")
    else:
        print("Book was not found. Database remains unchanged")




def help_delete_book():

    print("\n--- Delete a Book ---")

    book_id = read_positive_id()

    book = search_book_by_id(book_id)

    if book is None:
        print(f"Book was not found with ID: {book_id}")
        return

    print("\nBook to delete:")
    display_book(book)

    confirmation = input(
        "Are you sure you want to delete this book? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Delete was cancelled.")
        return

    deleted = delete_book(book_id)

    if deleted:
        print("Book deleted successfully!")
    else:
        print("Book was not found. Nothing was deleted.")


def display_menu():

    print("\n----------------------")
    print("LIBARY MANAGEMENT SYSTEM")
    print("\n----------------------")
    print("1. Add new book")
    print("2. View all books")
    print("3. Search book with ID")
    print("4. Update book")
    print("5. Delete book")
    print("6. Exit")





def main():
    options = {
        "1": help_add_book,
        "2": help_view_all_books,
        "3": help_search_book,
        "4": help_update_book,
        "5": help_delete_book
    }

    while True:
        display_menu()

        try:
            choice = input("\nChoose an option: ").strip()

            if choice == "6":
                print("\nThank you for using PostgreSQL Book Management System")
                break

            option = options.get(choice)

            if option is None:
                print("Invalid option. Please choose from list above.")
                continue

            option()

            
        except ValueError as e:
            print(f"\nInvalid input: {e}")

        except psycopg.Error:
            print(f"\nDatabase error. Try again")
        except ConnectionError:
            print(f"\nUnable to connect to database")

if __name__ == "__main__":
    main()