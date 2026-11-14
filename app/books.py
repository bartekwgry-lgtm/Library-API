"""HTTP endpoints for managing books."""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookRead, BookStatusUpdate, SixDigit

router = APIRouter(prefix="/books", tags=["books"])
DbSession = Annotated[AsyncSession, Depends(get_db)]


async def _get_book(db: AsyncSession, serial_number: str) -> Book:
    """Load a book by serial number.

    :param db: database session
    :param serial_number: 6-digit serial number
    :returns: matching book
    :raises HTTPException: 404 if the book does not exist
    """
    book = await db.get(Book, serial_number)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.get("", response_model=list[BookRead])
async def list_books(db: DbSession) -> list[Book]:
    """Return all books ordered by serial number.

    :param db: database session
    :returns: list of books
    """
    result = await db.execute(select(Book).order_by(Book.serial_number))
    return result.scalars().all()


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate, db: DbSession) -> Book:
    """Add a new available book.

    :param payload: book data including a unique serial number
    :param db: database session
    :returns: created book
    :raises HTTPException: 409 if the serial number already exists
    """
    if await db.get(Book, payload.serial_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book with this serial number already exists",
        )
    book = Book(
        serial_number=payload.serial_number,
        title=payload.title,
        author=payload.author,
        is_borrowed=False,
    )
    db.add(book)
    return book


@router.delete("/{serial_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(serial_number: SixDigit, db: DbSession) -> None:
    """Remove a book from the catalog.

    :param serial_number: 6-digit serial number
    :param db: database session
    :raises HTTPException: 404 if the book does not exist
    """
    book = await _get_book(db, serial_number)
    await db.delete(book)


@router.patch("/{serial_number}/status", response_model=BookRead)
async def update_book_status(
    serial_number: SixDigit, payload: BookStatusUpdate, db: DbSession
) -> Book:
    """Borrow or return a book.

    :param serial_number: 6-digit serial number
    :param payload: target loan status
    :param db: database session
    :returns: updated book
    :raises HTTPException: 404 if missing, 409 if already in the requested state
    """
    book = await _get_book(db, serial_number)
    if payload.is_borrowed:
        if book.is_borrowed:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Book is already borrowed",
            )
        book.is_borrowed = True
        book.borrowed_at = datetime.now(timezone.utc)
        book.borrower_card = payload.borrower_card
    else:
        if not book.is_borrowed:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Book is already available",
            )
        book.is_borrowed = False
        book.borrowed_at = None
        book.borrower_card = None
    return book
