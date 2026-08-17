"""Agregar DNI unico

Revision ID: b00aebdd5161
Revises: 
Create Date: 2026-08-05 18:53:04.145187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b00aebdd5161'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uq_users_dni', 'users', ['dni'])
    pass



def downgrade() -> None:
    op.drop_constraint('uq_users_dni', 'users', type_='unique')
    pass
