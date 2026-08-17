"""Hora creada el usuario

Revision ID: fbf3da308a7e
Revises: a07be8de2a22
Create Date: 2026-08-10 17:20:50.249958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'fbf3da308a7e'
down_revision: Union[str, Sequence[str], None] = 'a07be8de2a22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
  


def downgrade() -> None:
    op.drop_column('users', 'created_at')
    
