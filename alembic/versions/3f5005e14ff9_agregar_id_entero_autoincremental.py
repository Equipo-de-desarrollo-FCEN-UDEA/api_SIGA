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
    # Para user
    op.add_column('user', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS user_id_int_seq')
    op.execute("""UPDATE "user" SET id_int = nextval('user_id_int_seq')""")
    op.execute("""ALTER TABLE "user"
               ALTER COLUMN id_int
               SET DEFAULT nextval('user_id_int_seq')""")
    op.execute("""ALTER TABLE "user" ALTER COLUMN id_int SET NOT NULL""")
    op.execute("""ALTER SEQUENCE user_id_int_seq OWNED BY "user".id_int""")
    op.create_unique_constraint('uq_user_id_int', 'user', ['id_int'])

    # Para academic_unit
    op.add_column('academic_unit', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS academic_unit_id_int_seq')
    op.execute("""UPDATE academic_unit
               SET id_int = nextval('academic_unit_id_int_seq')""")
    op.execute("""ALTER TABLE academic_unit
               ALTER COLUMN id_int
               SET DEFAULT nextval('academic_unit_id_int_seq')""")
    op.execute("""ALTER TABLE academic_unit ALTER COLUMN id_int SET NOT NULL""")
    op.execute("""ALTER SEQUENCE academic_unit_id_int_seq
               OWNED BY academic_unit.id_int""")
    op.create_unique_constraint('uq_academic_unit_id_int', 'academic_unit', ['id_int'])

    # Para academic_unit_type
    op.add_column('academic_unit_type', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS academic_unit_type_id_int_seq')
    op.execute("""UPDATE academic_unit_type
               SET id_int = nextval('academic_unit_type_id_int_seq')""")
    op.execute("""ALTER TABLE academic_unit_type
                ALTER COLUMN id_int
                SET DEFAULT nextval('academic_unit_type_id_int_seq')""")
    op.execute("""ALTER TABLE academic_unit_type ALTER COLUMN id_int SET NOT NULL""")
    op.execute("""ALTER SEQUENCE academic_unit_type_id_int_seq
               OWNED BY academic_unit_type.id_int""")
    op.create_unique_constraint(
        'uq_academic_unit_type_id_int',
        'academic_unit_type',
        ['id_int'],
    )

    # Para application
    op.add_column('application', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS application_id_int_seq')
    op.execute("""UPDATE application SET id_int = nextval('application_id_int_seq')""")
    op.execute("""ALTER TABLE application
               ALTER COLUMN id_int
               SET DEFAULT nextval('application_id_int_seq')""")
    op.execute("""ALTER TABLE application ALTER COLUMN id_int SET NOT NULL""")
    op.execute("""ALTER SEQUENCE application_id_int_seq OWNED BY application.id_int""")
    op.create_unique_constraint('uq_application_id_int', 'application', ['id_int'])

    # Para rol
    op.add_column('rol', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS rol_id_int_seq')
    op.execute("""UPDATE rol SET id_int = nextval('rol_id_int_seq')""")
    op.execute("""ALTER TABLE rol
               ALTER COLUMN id_int
               SET DEFAULT nextval('rol_id_int_seq')""")
    op.execute("""ALTER TABLE rol ALTER COLUMN id_int SET NOT NULL""")
    op.execute("""ALTER SEQUENCE rol_id_int_seq OWNED BY rol.id_int""")
    op.create_unique_constraint('uq_rol_id_int', 'rol', ['id_int'])

    # Para status
    op.add_column('status', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS status_id_int_seq')
    op.execute("""UPDATE status SET id_int = nextval('status_id_int_seq')""")
    op.execute("""ALTER TABLE status
               ALTER COLUMN id_int
               SET DEFAULT nextval('status_id_int_seq')""")
    op.execute("""ALTER TABLE status ALTER COLUMN id_int SET NOT NULL""")
    op.execute("""ALTER SEQUENCE status_id_int_seq OWNED BY status.id_int""")
    op.create_unique_constraint('uq_status_id_int', 'status', ['id_int'])

    # Para user_application
    op.add_column('user_application', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS user_application_id_int_seq')
    op.execute(
        """UPDATE user_application
        SET id_int = nextval('user_application_id_int_seq')""",
    )
    op.execute("""ALTER TABLE user_application
               ALTER COLUMN id_int
               SET DEFAULT nextval('user_application_id_int_seq')""")
    op.execute("""ALTER TABLE user_application ALTER COLUMN id_int SET NOT NULL""")
    op.execute(
        """ALTER SEQUENCE user_application_id_int_seq
        OWNED BY user_application.id_int""",
    )
    op.create_unique_constraint(
        'uq_user_application_id_int',
        'user_application', ['id_int'],
    )

    # Para vote_type
    op.add_column('vote_type', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS vote_type_id_int_seq')
    op.execute("""UPDATE vote_type SET id_int = nextval('vote_type_id_int_seq')""")
    op.execute("""ALTER TABLE vote_type
               ALTER COLUMN id_int
               SET DEFAULT nextval('vote_type_id_int_seq')""")
    op.execute("""ALTER TABLE vote_type ALTER COLUMN id_int SET NOT NULL""")
    op.execute("""ALTER SEQUENCE vote_type_id_int_seq OWNED BY vote_type.id_int""")
    op.create_unique_constraint('uq_vote_type_id_int', 'vote_type', ['id_int'])

    # Para voting
    op.add_column('voting', sa.Column('id_int', sa.Integer(), nullable=True))
    op.execute('CREATE SEQUENCE IF NOT EXISTS voting_id_int_seq')
    op.execute("""UPDATE voting SET id_int = nextval('voting_id_int_seq')""")
    op.execute("""ALTER TABLE voting
               ALTER COLUMN id_int
               SET DEFAULT nextval('voting_id_int_seq')""")
    op.execute("""ALTER TABLE voting ALTER COLUMN id_int SET NOT NULL""")
    op.execute("""ALTER SEQUENCE voting_id_int_seq OWNED BY voting.id_int""")
    op.create_unique_constraint('uq_voting_id_int', 'voting', ['id_int'])


def downgrade() -> None:
    # Revertir para voting
    op.drop_constraint('uq_voting_id_int', 'voting', type_='unique')
    op.drop_column('voting', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS voting_id_int_seq')

    # Revertir para vote_type
    op.drop_constraint('uq_vote_type_id_int', 'vote_type', type_='unique')
    op.drop_column('vote_type', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS vote_type_id_int_seq')

    # Revertir para user_application
    op.drop_constraint('uq_user_application_id_int', 'user_application', type_='unique')
    op.drop_column('user_application', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS user_application_id_int_seq')

    # Revertir para status
    op.drop_constraint('uq_status_id_int', 'status', type_='unique')
    op.drop_column('status', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS status_id_int_seq')

    # Revertir para rol
    op.drop_constraint('uq_rol_id_int', 'rol', type_='unique')
    op.drop_column('rol', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS rol_id_int_seq')

    # Revertir para application
    op.drop_constraint('uq_application_id_int', 'application', type_='unique')
    op.drop_column('application', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS application_id_int_seq')

    # Revertir para academic_unit_type
    op.drop_constraint(
        'uq_academic_unit_type_id_int',
        'academic_unit_type', type_='unique',
    )
    op.drop_column('academic_unit_type', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS academic_unit_type_id_int_seq')

    # Revertir para academic_unit
    op.drop_constraint('uq_academic_unit_id_int', 'academic_unit', type_='unique')
    op.drop_column('academic_unit', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS academic_unit_id_int_seq')

    # Revertir para user
    op.drop_constraint('uq_user_id_int', 'user', type_='unique')
    op.drop_column('user', 'id_int')
    op.execute('DROP SEQUENCE IF EXISTS user_id_int_seq')
