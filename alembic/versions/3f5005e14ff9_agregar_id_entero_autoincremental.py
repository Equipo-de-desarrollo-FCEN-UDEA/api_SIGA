"""Agregar ID entero autoincremental

Revision ID: 3f5005e14ff9
Revises: b50021caa067
Create Date: 2025-06-24 14:24:51.283177

"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]
# from typing import Union


# revision identifiers, used by Alembic.
revision: str = '3f5005e14ff9'
down_revision: str | None = 'b50021caa067'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Añadir nueva columna `id_int`
    op.add_column('user', sa.Column('id_int', sa.Integer(), nullable=False))
    op.execute('CREATE SEQUENCE IF NOT EXISTS user_id_int_seq')
    op.execute("""ALTER TABLE user ALTER COLUMN id_int SET DEFAULT
               nextval('user_id_int_seq')""")
    op.execute("UPDATE user SET id_int = nextval('user_id_int_seq')")
    op.execute('ALTER SEQUENCE user_id_int_seq OWNED BY user.id_int')

    # 3. Eliminar la clave primaria actual (UUID)
    op.drop_constraint('user_pkey', 'user', type_='primary')

    # 4. Hacer `id_int` la nueva clave primaria
    op.create_primary_key('user_pkey', 'user', ['id_int'])

    # 5. Asegurar que el UUID siga siendo único
    op.create_unique_constraint('uq_user_uuid', 'user', ['id'])

    # 6. (Opcional) Renombrar columnas si lo deseas
    # op.alter_column('user', 'id', new_column_name='uuid')
    # op.alter_column('user', 'id_int', new_column_name='id')


def downgrade():
    pass
