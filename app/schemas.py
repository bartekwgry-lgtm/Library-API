"""Pydantic schemas for the books API."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

SixDigit = Annotated[str, Field(pattern=r"^\d{6}$", examples=["123456"])]


class BookCreate(BaseModel):
    """Payload for adding a book.

    :ivar serial_number: unique 6-digit serial number
    :ivar title: book title
    :ivar author: book author
    """

    serial_number: SixDigit
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)


class BookStatusUpdate(BaseModel):
    """Payload for borrowing or returning a book.

    :ivar is_borrowed: ``True`` to borrow, ``False`` to return
    :ivar borrower_card: 6-digit library card; required when borrowing
    """

    is_borrowed: bool
    borrower_card: SixDigit | None = None

    @model_validator(mode="after")
    def card_required_when_borrowing(self) -> "BookStatusUpdate":
        """Require a library card when borrowing and clear it when returning.

        :returns: validated payload
        :raises ValueError: if borrowing without ``borrower_card``
        """
        if self.is_borrowed and self.borrower_card is None:
            raise ValueError("borrower_card is required when borrowing a book")
        if not self.is_borrowed:
            self.borrower_card = None
        return self


class BookRead(BaseModel):
    """Book representation returned by the API.

    :ivar serial_number: unique 6-digit serial number
    :ivar title: book title
    :ivar author: book author
    :ivar is_borrowed: whether the book is currently on loan
    :ivar borrowed_at: UTC timestamp of the current loan, if any
    :ivar borrower_card: 6-digit library card of the current borrower
    """

    model_config = ConfigDict(from_attributes=True)

    serial_number: str
    title: str
    author: str
    is_borrowed: bool
    borrowed_at: datetime | None
    borrower_card: str | None
