"""Agregar Passoword a usuario

Revision ID: a07be8de2a22
Revises: b00aebdd5161
Create Date: 2026-08-06 19:14:19.164999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a07be8de2a22'
down_revision: Union[str, Sequence[str], None] = 'b00aebdd5161'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.add_column(
        "users",
        sa.Column("password", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "password")
