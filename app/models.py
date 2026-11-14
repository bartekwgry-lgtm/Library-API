"""ORM models."""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    """A library book identified by a 6-digit serial number.

    :ivar serial_number: unique 6-digit serial number
    :ivar title: book title
    :ivar author: book author
    :ivar is_borrowed: whether the book is currently on loan
    :ivar borrowed_at: UTC timestamp of the current loan, if any
    :ivar borrower_card: 6-digit library card of the current borrower
    """

    __tablename__ = "books"

    serial_number: Mapped[str] = mapped_column(String(6), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    is_borrowed: Mapped[bool] = mapped_column(default=False)
    borrowed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    borrower_card: Mapped[str | None] = mapped_column(String(6))
