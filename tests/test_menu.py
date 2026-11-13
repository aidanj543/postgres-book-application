
from decimal import Decimal

import psycopg
import pytest

import main


SAMPLE_BOOK = {
    "book_id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "category": "Programming",
    "published_year": 2008,
    "price": Decimal("35.00"),
}


def mock_inputs(monkeypatch, values):
    """Replace input() with predefined user responses."""

    responses = iter(values)
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(responses)
    )


def test_exit_menu(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["6"])

    main.main()

    output = capsys.readouterr().out
    assert "LIBRARY MANAGEMENT SYSTEM" in output
    assert "Thank you" in output


def test_invalid_menu_option(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["9", "6"])

    main.main()

    output = capsys.readouterr().out
    assert "Invalid option" in output
    assert "Thank you" in output


def test_add_book(monkeypatch, capsys):
    mock_inputs(monkeypatch, [
        "1",
        "Clean Code",
        "Robert C. Martin",
        "Programming",
        "2008",
        "35.00",
        "6",
    ])

    calls = []

    def fake_add(*args):
        calls.append(args)
        return 10

    monkeypatch.setattr(main, "add_book", fake_add)

    main.main()

    output = capsys.readouterr().out
    assert "Book added successfully" in output
    assert calls == [(
        "Clean Code",
        "Robert C. Martin",
        "Programming",
        2008,
        Decimal("35.00"),
    )]


def test_view_all_books(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["2", "6"])

    monkeypatch.setattr(
        main, "view_all_books", lambda: [SAMPLE_BOOK]
    )

    main.main()

    output = capsys.readouterr().out
    assert "Clean Code" in output
    assert "Robert C. Martin" in output
    assert "$35.00" in output


def test_view_empty_library(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["2", "6"])

    monkeypatch.setattr(
        main, "view_all_books", lambda: []
    )

    main.main()

    output = capsys.readouterr().out
    assert "No books found" in output


def test_search_book(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["3", "1", "6"])

    monkeypatch.setattr(
        main,
        "search_book_by_id",
        lambda book_id: SAMPLE_BOOK,
    )

    main.main()

    output = capsys.readouterr().out
    assert "Clean Code" in output


def test_search_missing_book(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["3", "999", "6"])

    monkeypatch.setattr(
        main,
        "search_book_by_id",
        lambda book_id: None,
    )

    main.main()

    output = capsys.readouterr().out
    assert "was not found" in output


def test_update_book(monkeypatch, capsys):
    mock_inputs(monkeypatch, [
        "4",
        "1",
        "Updated Clean Code",
        "Robert C. Martin",
        "Programming",
        "2008",
        "40.00",
        "6",
    ])

    monkeypatch.setattr(
        main,
        "search_book_by_id",
        lambda book_id: SAMPLE_BOOK,
    )

    calls = []

    def fake_update(*args):
        calls.append(args)
        return True

    monkeypatch.setattr(main, "update_book", fake_update)

    main.main()

    output = capsys.readouterr().out
    assert "Book updated successfully" in output
    assert calls[0][0] == 1
    assert calls[0][1] == "Updated Clean Code"
    assert calls[0][-1] == Decimal("40.00")


def test_delete_book_confirmed(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["5", "1", "y", "6"])

    monkeypatch.setattr(
        main,
        "search_book_by_id",
        lambda book_id: SAMPLE_BOOK,
    )

    deleted_ids = []

    def fake_delete(book_id):
        deleted_ids.append(book_id)
        return True

    monkeypatch.setattr(main, "delete_book", fake_delete)

    main.main()

    output = capsys.readouterr().out
    assert "Book deleted successfully" in output
    assert deleted_ids == [1]


def test_delete_cancelled(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["5", "1", "n", "6"])

    monkeypatch.setattr(
        main,
        "search_book_by_id",
        lambda book_id: SAMPLE_BOOK,
    )

    def should_not_delete(book_id):
        pytest.fail("delete_book should not be called")

    monkeypatch.setattr(
        main, "delete_book", should_not_delete
    )

    main.main()

    output = capsys.readouterr().out
    assert "Deletion cancelled" in output


def test_invalid_book_id(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["3", "abc", "6"])

    main.main()

    output = capsys.readouterr().out
    assert "Invalid input" in output
    assert "Thank you" in output


def test_invalid_book_year(monkeypatch, capsys):
    mock_inputs(monkeypatch, [
        "1", "Test", "Author", "Fiction", "abc", "6"
    ])

    main.main()

    output = capsys.readouterr().out
    assert "Published year must be an integer" in output


def test_database_error(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["2", "6"])

    def fake_view():
        raise psycopg.OperationalError(
            "Simulated database problem"
        )

    monkeypatch.setattr(
        main, "view_all_books", fake_view
    )

    main.main()

    output = capsys.readouterr().out
    assert "Database error" in output
    assert "Thank you" in output


def test_connection_error(monkeypatch, capsys):
    mock_inputs(monkeypatch, ["2", "6"])

    def fake_view():
        raise ConnectionError("Simulated connection failure")

    monkeypatch.setattr(
        main, "view_all_books", fake_view
    )

    main.main()

    output = capsys.readouterr().out
    assert "Unable to connect" in output
    assert "Thank you" in output
