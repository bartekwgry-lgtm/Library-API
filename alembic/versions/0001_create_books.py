"""create books table

Revision ID: 0001_create_books
Revises:
Create Date: 2026-11-14
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "0001_create_books"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("serial_number", sa.String(length=6), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=False),
        sa.Column("is_borrowed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("borrowed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("borrower_card", sa.String(length=6), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("books")
