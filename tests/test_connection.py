
import os

import pytest

from database import get_connection


def test_database_connection():
    """Verify that Python can connect to library_db."""

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user;"
            )

            database_name, username = cursor.fetchone()

            assert database_name == "library_db"
            assert username == os.getenv("DB_USER")


def test_books_table_exists():
    """Verify that the books table exists."""

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT to_regclass('public.books');"
            )

            result = cursor.fetchone()

            assert result[0] == "books"


def test_missing_database_configuration(monkeypatch):
    """Check that missing credentials raise an error."""

    monkeypatch.delenv("DB_PASSWORD", raising=False)

    with pytest.raises(ValueError, match="DB_PASSWORD"):
        get_connection()
