# test_base_router.py
from __future__ import annotations

from typing import List
from typing import Type
from uuid import UUID
from uuid import uuid4

import pytest
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.api.base_router import BaseRouter
from app.api.middleware.postgres_db import get_db

# Esquemas de prueba


class TestSchemaInDB(BaseModel):
    id: UUID
    name: str


class TestSchemaCreate(BaseModel):
    name: str


class TestSchemaUpdate(BaseModel):
    name: str

# Servicio de prueba


class TestService:
    def __init__(self):
        self.db = []

    def create(self, obj_in: TestSchemaCreate, db):
        obj = TestSchemaInDB(id=uuid4(), name=obj_in.name)
        self.db.append(obj)
        return obj

    def get_multi(self, skip: int, limit: int, db):
        return self.db[skip:skip+limit]

    def get(self, id: UUID, db):
        for obj in self.db:
            if obj.id == id:
                return obj
        return None

    def update(self, id: UUID, obj_in: TestSchemaUpdate, db):
        for obj in self.db:
            if obj.id == id:
                obj.name = obj_in.name
                return obj
        raise HTTPException(status_code=404, detail='entity not found')


# Configuración del router y BaseRouter
router = APIRouter()
service = TestService()
base_router = BaseRouter(
    schem_in_db=TestSchemaInDB,
    schem_create=TestSchemaCreate,
    schem_update=TestSchemaUpdate,
    service=service,
    router=router,
)

# Cliente de prueba
client = TestClient(router)

# Pruebas


def test_create():
    response = client.post('/create', json={'name': 'test entity'})
    assert response.status_code == 201
    assert response.json()['name'] == 'test entity'


def test_get_all():
    response = client.get('/get-all')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get():
    entity = service.create(
        obj_in=TestSchemaCreate(name='test entity'), db=None,
    )
    response = client.get(f'/get/{entity.id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'test entity'


def test_update():
    entity = service.create(
        obj_in=TestSchemaCreate(name='test entity'), db=None,
    )
    response = client.patch(
        f'/update/{entity.id}', json={'name': 'updated entity'},
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'entity updated'
    updated_entity = service.get(id=entity.id, db=None)
    assert updated_entity.name == 'updated entity'
