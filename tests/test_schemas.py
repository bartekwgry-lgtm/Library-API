import pytest
from pydantic import ValidationError

from app.schemas import BookCreate, BookStatusUpdate


def test_book_create_accepts_six_digit_serial() -> None:
    book = BookCreate(serial_number="123456", title="Solaris", author="Stanisław Lem")
    assert book.serial_number == "123456"


@pytest.mark.parametrize("serial_number", ["12345", "1234567", "12345a", ""])
def test_book_create_rejects_invalid_serial(serial_number: str) -> None:
    with pytest.raises(ValidationError):
        BookCreate(serial_number=serial_number, title="Solaris", author="Stanisław Lem")


def test_borrow_requires_card() -> None:
    with pytest.raises(ValidationError, match="borrower_card is required"):
        BookStatusUpdate(is_borrowed=True)


def test_return_clears_card() -> None:
    update = BookStatusUpdate(is_borrowed=False, borrower_card="654321")
    assert update.borrower_card is None
