from __future__ import annotations

from uuid import UUID

import pytest
from pydantic import ValidationError

from app.schemas.users.type.administrative import AdministrativeBase
from app.schemas.users.type.administrative import AdministrativeType
from app.schemas.users.type.administrative import ContractType


def test_contract_type_valid_values():
    assert ContractType.CARRERA_ADMINISTRATIVA == 'CARRERA_ADMINISTRATIVA'
    assert ContractType.LIBRE_NOMBRAMIENTO_REMOSION == 'LIBRE_NOMBRAMIENTO_REMOSION'
    assert ContractType.PROVISIONAL == 'PROVISIONAL'
    assert ContractType.TEMPORAL == 'TEMPORAL'
    assert ContractType.CIS == 'CIS'


def test_contract_type_invalid_value():
    with pytest.raises(ValueError):
        ContractType('INVALID_VALUE')

        def test_administrative_type_valid_values():
            assert AdministrativeType.SECRETARIA == 'SECRETARIA'
            assert AdministrativeType.SECRETARIO == 'SECRETARIO'
            assert AdministrativeType.ALMACENISTA == 'ALMACENISTA'
            assert AdministrativeType.COORDINADOR == 'COORDINADOR'
            assert AdministrativeType.DIRECTOR == 'DIRECTOR'

        def test_administrative_type_invalid_value():
            with pytest.raises(ValueError):
                AdministrativeType('INVALID_VALUE')

        def test_administrative_base_valid_data():
            valid_data = {
                'id_postgres': '123e4567-e89b-12d3-a456-426614174000',
                'type': 'SECRETARIA',
                'contract': 'CARRERA_ADMINISTRATIVA',
            }
            administrative_base = AdministrativeBase(**valid_data)
            assert administrative_base.id_postgres == UUID(
                '123e4567-e89b-12d3-a456-426614174000',
            )
            assert administrative_base.type == AdministrativeType.SECRETARIA
            assert administrative_base.contract == ContractType.CARRERA_ADMINISTRATIVA

        def test_administrative_base_invalid_data():
            invalid_data = {
                'id_postgres': 'invalid-uuid',
                'type': 'INVALID_TYPE',
                'contract': 'INVALID_CONTRACT',
            }
            with pytest.raises(ValidationError):
                AdministrativeBase(**invalid_data)
