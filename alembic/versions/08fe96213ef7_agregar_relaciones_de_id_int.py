"""Agregar relaciones de ID entero

Revision ID: 08fe96213ef7
Revises: 3f5005e14ff9
Create Date: 2025-06-25 14:45:31.471316

"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]


# revision identifiers, used by Alembic.
revision: str = '08fe96213ef7'
down_revision: str | None = '3f5005e14ff9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def add_fk_int_column(
    *,
    table: str,
    column_uuid: str,
    column_int: str,
    ref_table: str,
    fk_name: str,
    index: bool = True,
    alias_table: str = 't',
    alias_ref: str = 'r',
    ondelete: str = 'SET NULL',
):
    op.add_column(table, sa.Column(column_int, sa.Integer(), nullable=True))
    real_ref_table = f'"{ref_table}"'
    op.execute(f"""
        UPDATE {table} {alias_table}
        SET {column_int} = {alias_ref}.id_int
        FROM {real_ref_table} {alias_ref}
        WHERE {alias_table}.{column_uuid} = {alias_ref}.id
    """)
    op.create_foreign_key(
        fk_name,
        source_table=table,
        referent_table=ref_table,
        local_cols=[column_int],
        remote_cols=['id_int'],
        ondelete=ondelete,
    )
    if index:
        op.create_index(f'ix_{table}_{column_int}', table, [column_int])


def upgrade():
    # ========== Para academic_unit =============
    add_fk_int_column(
        table='academic_unit',
        column_uuid='academic_unit_type_id',
        column_int='academic_unit_type_id_int',
        ref_table='academic_unit_type',
        fk_name='fk_academic_unit_academic_unit_type_id_int',
        index=True,
    )
    add_fk_int_column(
        table='academic_unit',
        column_uuid='academic_unit_id',
        column_int='academic_unit_id_int',
        ref_table='academic_unit',
        fk_name='fk_academic_unit_academic_unit_id_int',
        index=True,
    )

    # ========= Para academic_unit_type ============
    add_fk_int_column(
        table='application',
        column_uuid='academic_unit_id',
        column_int='academic_unit_id_int',
        ref_table='academic_unit',
        fk_name='fk_application_academic_unit_id_int',
        index=True,
    )

    # ======== Para application =============
    add_fk_int_column(
        table='application_status',
        column_uuid='application_id',
        column_int='application_id_int',
        ref_table='application',
        fk_name='fk_application_status_application_id_int',
        index=False,
    )
    add_fk_int_column(
        table='application_status',
        column_uuid='status_id',
        column_int='status_id_int',
        ref_table='status',
        fk_name='fk_application_status_status_id_int',
        index=False,
    )

    # ======== Para rol ============
    add_fk_int_column(
        table='rol',
        column_uuid='academic_unit_id',
        column_int='academic_unit_id_int',
        ref_table='academic_unit',
        fk_name='fk_rol_academic_unit_id_int',
        index=True,
    )

    # ======== Para user_application ============
    add_fk_int_column(
        table='user_application',
        column_uuid='user_id',
        column_int='user_id_int',
        ref_table='user',
        fk_name='fk_user_application_user_id_int',
        index=True,
    )
    add_fk_int_column(
        table='user_application',
        column_uuid='application_id',
        column_int='application_id_int',
        ref_table='application',
        fk_name='fk_user_application_application_id_int',
        index=True,
    )

    # ======== Para user_application_academic_unit ============
    add_fk_int_column(
        table='user_application_academic_unit',
        column_uuid='user_application_id',
        column_int='user_application_id_int',
        ref_table='user',
        fk_name='fk_user_application_academic_unit_user_application_id_int',
        index=True,
    )
    add_fk_int_column(
        table='user_application_academic_unit',
        column_uuid='academic_unit_id',
        column_int='academic_unit_id_int',
        ref_table='academic_unit',
        fk_name='fk_user_application_academic_unit_academic_unit_id_int',
        index=True,
    )

    # ======== Para user_application_status ============
    add_fk_int_column(
        table='user_application_status',
        column_uuid='user_application_id',
        column_int='user_application_id_int',
        ref_table='user_application',
        fk_name='fk_user_application_status_user_application_id_int',
        index=True,
    )
    add_fk_int_column(
        table='user_application_status',
        column_uuid='status_id',
        column_int='status_id_int',
        ref_table='status',
        fk_name='fk_user_application_status_status_id_int',
        index=False,
    )

    # ======== Para user_application_user ============
    add_fk_int_column(
        table='user_application_user',
        column_uuid='user_id',
        column_int='user_id_int',
        ref_table='user',
        fk_name='fk_user_application_user_user_id_int',
        index=True,
    )
    add_fk_int_column(
        table='user_application_user',
        column_uuid='user_application_id',
        column_int='user_application_id_int',
        ref_table='user_application',
        fk_name='fk_user_application_user_user_application_id_int',
        index=True,
    )

    # ======== Para user_rol_academic_unit ============
    add_fk_int_column(
        table='user_rol_academic_unit',
        column_uuid='user_id',
        column_int='user_id_int',
        ref_table='user',
        fk_name='fk_user_rol_academic_unit_user_id_int',
        index=True,
    )
    add_fk_int_column(
        table='user_rol_academic_unit',
        column_uuid='rol_id',
        column_int='rol_id_int',
        ref_table='rol',
        fk_name='fk_user_rol_academic_unit_rol_id_int',
        index=True,
    )
    add_fk_int_column(
        table='user_rol_academic_unit',
        column_uuid='academic_unit_id',
        column_int='academic_unit_id_int',
        ref_table='academic_unit',
        fk_name='fk_user_rol_academic_unit_academic_unit_id_int',
        index=True,
    )

    # ======== Para vote ============
    add_fk_int_column(
        table='vote',
        column_uuid='user_id',
        column_int='user_id_int',
        ref_table='user',
        fk_name='fk_vote_user_id_int',
        index=True,
    )
    add_fk_int_column(
        table='vote',
        column_uuid='voting_id',
        column_int='voting_id_int',
        ref_table='voting',
        fk_name='fk_vote_voting_id_int',
        index=True,
    )
    add_fk_int_column(
        table='vote',
        column_uuid='vote_type_id',
        column_int='vote_type_id_int',
        ref_table='vote_type',
        fk_name='fk_vote_vote_type_id_int',
        index=True,
    )

    # ======== Para voting ============
    add_fk_int_column(
        table='voting',
        column_uuid='academic_unit_id',
        column_int='academic_unit_id_int',
        ref_table='academic_unit',
        fk_name='fk_voting_academic_unit_id_int',
        index=True,
    )
    add_fk_int_column(
        table='voting',
        column_uuid='user_application_id',
        column_int='user_application_id_int',
        ref_table='user_application',
        fk_name='fk_voting_user_application_id_int',
        index=True,
    )


def downgrade():
    # Lista de columnas agregadas, en orden inverso al upgrade
    columns_to_remove = [
        # voting
        ('voting', 'user_application_id_int', 'fk_voting_user_application_id_int', True),
        ('voting', 'academic_unit_id_int', 'fk_voting_academic_unit_id_int', True),
        # vote
        ('vote', 'vote_type_id_int', 'fk_vote_vote_type_id_int', True),
        ('vote', 'voting_id_int', 'fk_vote_voting_id_int', True),
        ('vote', 'user_id_int', 'fk_vote_user_id_int', True),
        # user_rol_academic_unit
        (
            'user_rol_academic_unit', 'academic_unit_id_int',
            'fk_user_rol_academic_unit_academic_unit_id_int', True,
        ),
        (
            'user_rol_academic_unit', 'rol_id_int',
            'fk_user_rol_academic_unit_rol_id_int', True,
        ),
        (
            'user_rol_academic_unit', 'user_id_int',
            'fk_user_rol_academic_unit_user_id_int', True,
        ),
        # user_application_user
        (
            'user_application_user', 'user_application_id_int',
            'fk_user_application_user_user_application_id_int', True,
        ),
        (
            'user_application_user', 'user_id_int',
            'fk_user_application_user_user_id_int', True,
        ),
        # user_application_status
        (
            'user_application_status', 'status_id_int',
            'fk_user_application_status_status_id_int', False,
        ),
        (
            'user_application_status', 'user_application_id_int',
            'fk_user_application_status_user_application_id_int', True,
        ),
        # user_application_academic_unit
        (
            'user_application_academic_unit', 'academic_unit_id_int',
            'fk_user_application_academic_unit_academic_unit_id_int', True,
        ),
        (
            'user_application_academic_unit', 'user_application_id_int',
            'fk_user_application_academic_unit_user_application_id_int', True,
        ),
        # user_application
        (
            'user_application', 'application_id_int',
            'fk_user_application_application_id_int', True,
        ),
        ('user_application', 'user_id_int', 'fk_user_application_user_id_int', True),
        # rol
        ('rol', 'academic_unit_id_int', 'fk_rol_academic_unit_id_int', False),
        # application_status
        (
            'application_status', 'status_id_int',
            'fk_application_status_status_id_int', False,
        ),
        (
            'application_status', 'application_id_int',
            'fk_application_status_application_id_int', False,
        ),
        # application
        (
            'application', 'academic_unit_id_int',
            'fk_application_academic_unit_id_int', False,
        ),
        # academic_unit
        (
            'academic_unit', 'academic_unit_id_int',
            'fk_academic_unit_academic_unit_id_int', True,
        ),
        (
            'academic_unit', 'academic_unit_type_id_int',
            'fk_academic_unit_academic_unit_type_id_int', True,
        ),
    ]

    for table, column, fk_name, has_index in columns_to_remove:
        op.drop_constraint(fk_name, table_name=table, type_='foreignkey')
        if has_index:
            op.drop_index(f'ix_{table}_{column}', table_name=table)
        op.drop_column(table, column)
