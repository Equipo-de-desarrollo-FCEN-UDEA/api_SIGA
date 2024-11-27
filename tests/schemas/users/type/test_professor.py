from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import pytest

from app.schemas.users.type.professor import ProfessorBase
from app.schemas.users.type.professor import ProfessorCreate
from app.schemas.users.type.professor import ProfessorInDB
from app.schemas.users.type.professor import ProfessorResponse
from app.schemas.users.type.professor import ProfessorType
from app.schemas.users.type.professor import ProfessorUpdate
from app.schemas.users.user import IdentificationType
from app.schemas.users.user import UserInDB


def test_professor_base():
    professor = ProfessorBase(
        id_postgres=uuid4(), type=ProfessorType.VINCULADO,
    )
    assert professor.type == ProfessorType.VINCULADO


def test_professor_create():
    professor = ProfessorCreate(
        id_postgres=uuid4(), type=ProfessorType.OCACIONAL,
    )
    assert professor.type == ProfessorType.OCACIONAL


def test_professor_update():
    professor = ProfessorUpdate()
    assert professor is not None


def test_professor_in_db():
    professor = ProfessorInDB(
        id_postgres=uuid4(),
        type=ProfessorType.CATEDRATICO,
    )
    assert professor.type == ProfessorType.CATEDRATICO


def test_professor_response():
    user = UserInDB(
        id=uuid4(),
        name='Test',
        last_name='User',
        email='test@example.com',
        identification_type=IdentificationType.CEDULA_CIUDADANIA,
        identification_number='123456789',
        phone='1234567890',
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    professor_in_db = ProfessorInDB(
        id_postgres=uuid4(), type=ProfessorType.VINCULADO,
    )
    response = ProfessorResponse(
        id=user.id,
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        identification_type=user.identification_type,
        identification_number=user.identification_number,
        phone=user.phone,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        professor=professor_in_db,
    )
    assert response.professor.type == ProfessorType.VINCULADO
