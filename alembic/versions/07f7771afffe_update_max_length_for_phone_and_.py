"""update max length for phone and identification number

Revision ID: 07f7771afffe
Revises: 52e0bac1494b
Create Date: 2024-09-26 21:18:36.898964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07f7771afffe'
down_revision: Union[str, None] = '52e0bac1494b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user', 'phone', type_=sa.String(length=20))
    op.alter_column('user', 'identification_number', type_=sa.String(length=50))


def downgrade() -> None:
    op.alter_column('user', 'phone', type_=sa.String(length=10))
    op.alter_column('user', 'identification_number', type_=sa.String(length=10))
