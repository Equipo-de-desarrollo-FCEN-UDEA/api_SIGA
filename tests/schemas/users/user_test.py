from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.infraestructure.db.models.user.user import IdentificationType
from app.schemas.organization.academic_unit_type import AcademicUnitType
from app.schemas.users.user import User
from app.schemas.users.user import UserBase
from app.schemas.users.user import UserCreate
from app.schemas.users.user import UserCreateInDB
from app.schemas.users.user import UserInDB
from app.schemas.users.user import UserSearch
from app.schemas.users.user import UserUpdate
from app.schemas.users.user_rol_academic_unit import AcademicUnit
from app.schemas.users.user_rol_academic_unit import Rol
from app.schemas.users.user_rol_academic_unit import UserRolAcademicUnit

import hashlib
import binascii
from uuid import uuid4

def hash_password(password, salt):
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return binascii.hexlify(dk).decode()


def test_user_base():
    user = UserBase(
        name='Test',
        last_name='User',
        email='test@example.com',
        identification_type=IdentificationType.CEDULA_CIUDADANIA,
        identification_number='123456789',
        phone='1234567890',
        is_active=True,
    )
    assert user.name == 'Test'
    assert user.last_name == 'User'
    assert user.email == 'test@example.com'
    assert user.identification_type == IdentificationType.CEDULA_CIUDADANIA
    assert user.identification_number == '123456789'
    assert user.phone == '1234567890'
    assert user.is_active is True


def test_user_create():
    salt = 'somesalt'  # In a real scenario, use a unique salt for each password
    password = 'password123'
    hashed_password = hash_password(password, salt)

    user = UserCreate(
        name='Test',
        last_name='User',
        email='test@example.com',
        identification_type=IdentificationType.CEDULA_CIUDADANIA,
        identification_number='123456789',
        phone='1234567890',
        is_active=True,
        password=password,
    )
    assert user.password == password


def test_user_update():
    user_update = UserUpdate(
        email='newemail@example.com',
        name='NewName',
        last_name='NewLastName',
        is_active=False,
        phone='0987654321',
        identification_type=IdentificationType.PASAPORTE,
        identification_number='987654321',
    )
    assert user_update.email == 'newemail@example.com'
    assert user_update.name == 'NewName'
    assert user_update.last_name == 'NewLastName'
    assert user_update.is_active is False
    assert user_update.phone == '0987654321'
    assert user_update.identification_type == IdentificationType.PASAPORTE
    assert user_update.identification_number == '987654321'


def test_user_create_in_db():
    user = UserCreateInDB(
        name='Test',
        last_name='User',
        email='test@example.com',
        identification_type=IdentificationType.CEDULA_CIUDADANIA,
        identification_number='123456789',
        phone='1234567890',
        is_active=True,
        hashed_password =hash_password('hashedpassword123', 'somesalt'),
    )
    assert user.hashed_password == hash_password('hashedpassword123', 'somesalt')


def test_user_in_db():
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
    assert user.name == 'Test'
    assert user.last_name == 'User'
    assert user.email == 'test@example.com'
    assert user.identification_type == IdentificationType.CEDULA_CIUDADANIA
    assert user.identification_number == '123456789'
    assert user.phone == '1234567890'
    assert user.is_active is True


def test_user_search():
    user_search = UserSearch(
        names__icontains='Test',
        email__icontains='example.com',
    )
    assert user_search.names__icontains == 'Test'
    assert user_search.email__icontains == 'example.com'


def test_user():
    rol = Rol(id=uuid4(), name='Admin', description='PROFESOR')
    academic_unit_type = AcademicUnitType(id=uuid4(), name='INSTITUTO')
    academic_unit = AcademicUnit(
        id=uuid4(), name='Instituto de Física',
        academic_unit_type=academic_unit_type,
    )
    user_roles_academic_units = [
        UserRolAcademicUnit(
            rol=rol, academic_unit=academic_unit,
        ),
    ]
    user = User(
        id=uuid4(),
        name='Test',
        last_name='User',
        email='test@example.com',
        identification_type=IdentificationType.CEDULA_CIUDADANIA,
        identification_number='123456789',
        phone='1234567890',
        is_active=True,
        user_roles_academic_units=user_roles_academic_units,
    )
    assert user.name == 'Test'
    assert user.last_name == 'User'
    assert user.email == 'test@example.com'
    assert user.identification_type == IdentificationType.CEDULA_CIUDADANIA
    assert user.identification_number == '123456789'
    assert user.phone == '1234567890'
    assert user.is_active is True
    assert user.user_roles_academic_units == user_roles_academic_units
