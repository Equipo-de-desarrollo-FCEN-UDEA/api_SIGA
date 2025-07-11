"""add uuid_generate for academic_unit

Revision ID: 7da57a4632e3
Revises: c66f27d239f0
Create Date: 2024-10-03 18:50:45.868442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7da57a4632e3'
down_revision: Union[str, None] = 'c66f27d239f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Habilitar la extensión uuid-ossp
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Agregar el valor por defecto a la columna id
    op.alter_column('academic_unit', 'id', server_default=sa.text("uuid_generate_v4()"))

def downgrade():
    # Eliminar el valor por defecto de la columna id
    op.alter_column('academic_unit', 'id', server_default=None)
    
    # Opcional: Deshabilitar la extensión uuid-ossp si no se necesita
    # op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
