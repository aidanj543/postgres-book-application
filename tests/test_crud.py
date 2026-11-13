
from decimal import Decimal

import pytest

from database import (
    add_book,
    view_all_books,
    search_book_by_id,
    update_book,
    delete_book,
)


@pytest.fixture
def sample_book():
    """Create a test book and clean up afterward."""

    book_id = add_book(
        "Pytest Sample Book",
        "Test Author",
        "Testing",
        2024,
        "25.00",
    )

    try:
        yield book_id
    finally:
        # The test may have already deleted this record.
        delete_book(book_id)


def test_add_book():
    book_id = add_book(
        "New Test Book",
        "Test Author",
        "Programming",
        2025,
        "19.99",
    )

    try:
        book = search_book_by_id(book_id)

        assert book is not None
        assert book["title"] == "New Test Book"
        assert book["price"] == Decimal("19.99")
    finally:
        delete_book(book_id)


def test_view_all_books(sample_book):
    books = view_all_books()

    assert isinstance(books, list)
    assert any(
        book["book_id"] == sample_book
        for book in books
    )


def test_search_book_by_id(sample_book):
    book = search_book_by_id(sample_book)

    assert book is not None
    assert book["book_id"] == sample_book
    assert book["title"] == "Pytest Sample Book"


def test_search_nonexistent_book():
    # SERIAL IDs are positive; zero is not a valid ID,
    # so search for an ID unlikely to exist instead.
    assert search_book_by_id(2147483647) is None


def test_update_book(sample_book):
    result = update_book(
        sample_book,
        "Updated Test Book",
        "New Author",
        "Education",
        2025,
        "39.99",
    )

    book = search_book_by_id(sample_book)

    assert result is True
    assert book["title"] == "Updated Test Book"
    assert book["author"] == "New Author"
    assert book["price"] == Decimal("39.99")


def test_delete_book(sample_book):
    result = delete_book(sample_book)

    assert result is True
    assert search_book_by_id(sample_book) is None
    assert delete_book(sample_book) is False


@pytest.mark.parametrize("invalid_id", [-1, 0, "abc", None, True])
def test_invalid_book_id(invalid_id):
    with pytest.raises(ValueError):
        search_book_by_id(invalid_id)

    with pytest.raises(ValueError):
        delete_book(invalid_id)


@pytest.mark.parametrize(
    "title, author, category, year, price",
    [
        ("", "Author", "Programming", 2024, "10.00"),
        ("Book", "", "Programming", 2024, "10.00"),
        ("Book", "Author", "", 2024, "10.00"),
        ("Book", "Author", "Programming", "abc", "10.00"),
        ("Book", "Author", "Programming", 2024, "-5.00"),
        ("Book", "Author", "Programming", 2024, "19.999"),
    ],
)
def test_invalid_book_details(title, author, category, year, price):
    with pytest.raises(ValueError):
        add_book(title, author, category, year, price)


def test_update_nonexistent_book():
    result = update_book(
        2147483647,
        "Missing Book",
        "Nobody",
        "Testing",
        2025,
        "15.00",
    )

    assert result is False


def test_delete_nonexistent_book():
    assert delete_book(2147483647) is False


def test_parameterized_sql_handles_quotes():
    book_id = add_book(
        "O'Reilly's Python Guide",
        "Test Author",
        "Programming",
        2025,
        "20.00",
    )

    try:
        book = search_book_by_id(book_id)
        assert book["title"] == "O'Reilly's Python Guide"
    finally:
        delete_book(book_id)
