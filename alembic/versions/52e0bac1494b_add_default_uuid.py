"""add default UUID

Revision ID: 52e0bac1494b
Revises: 8d9373c7b13b
Create Date: 2024-09-26 20:42:01.906222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52e0bac1494b'
down_revision: Union[str, None] = '8d9373c7b13b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Habilitar la extensión uuid-ossp
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Agregar el valor por defecto a la columna id
    op.alter_column('user', 'id', server_default=sa.text("uuid_generate_v4()"))

def downgrade():
    # Eliminar el valor por defecto de la columna id
    op.alter_column('user', 'id', server_default=None)
    
    # Opcional: Deshabilitar la extensión uuid-ossp si no se necesita
    # op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
