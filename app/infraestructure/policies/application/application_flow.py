from __future__ import annotations

import re
from datetime import datetime
from typing import TypeAlias

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.constants import REJECTED_STATUS_ID
from app.infraestructure.db.models.application.application import Application
from app.infraestructure.db.models.application.application_status import (
    ApplicationStatus,
)
from app.infraestructure.db.models.application.user_application import UserApplication
from app.infraestructure.db.models.application.user_application_status import (
    UserApplicationStatus,
)
from app.infraestructure.db.models.voting.voting_info import VotingInfo
from app.schemas.application.user_application_academic_unit import (
    UserApplicationAcademicUnitCreate,
)
from app.schemas.application.user_application_status import UserApplicationStatusCreate
from app.schemas.application.user_application_user import UserApplicationUserCreate
from app.schemas.voting.voting import VotingCreate
from app.schemas.voting.voting_info import VotingInfoCreate
from app.schemas.voting.voting_info import VotingStatus
from app.services.application.user_application_academic_unit import (
    user_application_academic_unit_svc,
)
from app.services.application.user_application_status import user_application_status_svc
from app.services.application.user_application_user import user_application_user_svc
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc
from app.services.voting.voting import voting_svc
from app.services.voting.voting_info import voting_info_svc


class ApplicationFlow:
    def __init__(self, user_application: UserApplication):
        self.user_application = user_application

    # Función que elimina caracteres especiales
    def extract_params(self, param_str):
        if not re.match(r'^[\w\s=,"-]*$', param_str):
            raise ValueError('Invalid characters in parameter string')

        params = param_str.split(',')
        param_matches = []
        for param in params:
            parts = param.split('=')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip().strip('"').replace('\\"', '"')
                if re.match(r'^\w+$', key):
                    param_matches.append((key, value))

        return param_matches

    def get_action(self, is_approved) -> str | None:
        """
        Obtiene el siguiente estado válido según la transición permitida.
        :param current_status: Estado actual de la aplicación.
        :param is_approved: Indica si la transición es aprobada.
        :return: Nombre del siguiente estado.
        """

        if not is_approved:
            return 'reject'

        # Solo es para tipar más corto
        UAS: TypeAlias = UserApplicationStatus

        application: Application = self.user_application.application
        current_status: UAS = self.user_application.user_application_status[0]
        application_status: list[ApplicationStatus] = application.application_status

        for app_status in application_status:
            if app_status.status_id == current_status.status_id:
                return app_status.action

        return None

    async def next(self, **kwargs):
        """
        Avanza al siguiente estado según la transición definida.
        :param user_application_id: ID de la aplicación del usuario.
        :param db_mongo: Conexión a MongoDB.
        :param db_postgres: Conexión a PostgreSQL.
        :param current_user: Usuario que ejecuta la acción.
        :return: Respuesta de la acción ejecutada.
        """

        action = self.get_action(
            kwargs.get('is_approved'),
        )

        if action is None:
            raise HTTPException(status_code=400, detail='Invalid transition')

        patterns = re.match(r'(\w+)(?:\((.*)\))?', action)

        if not patterns:
            return await getattr(self, action)(**kwargs)

        action_name, param_str = patterns.groups()

        parsed_params = {}
        if param_str:
            # Busca `param = "value"`
            param_matches = self.extract_params(param_str)
            parsed_params = {key: value for key, value in param_matches}

        return await getattr(self, action_name)(**{**kwargs, **parsed_params})

    def get_next_status(
            self,
            updated_by,
            observation,
            jump: int = 0,
    ) -> UserApplicationStatusCreate | None:

        # Solo es para tipar más corto
        UAS: TypeAlias = UserApplicationStatus

        application: Application = self.user_application.application
        current_status: UAS = self.user_application.user_application_status[0]
        application_status: list[ApplicationStatus] = application.application_status

        for app_status in application_status:
            if app_status.status_id == current_status.status_id:
                current_step = app_status.step
                break

        for app_status in application_status:
            if app_status.step == current_step + 1 + jump:
                next_status = app_status.status
                break

        return UserApplicationStatusCreate(
            user_application_id=self.user_application.id,
            status_id=next_status.id,
            updated_by=updated_by,
            observation=observation,
        )

    async def next_status(self, **kwargs):
        db_postgres = kwargs.get('db_postgres')
        jump = int(kwargs.get('jump', 0))

        user_application_status = self.get_next_status(
            updated_by=kwargs.get('current_user').id,
            observation=kwargs.get('observation'),
            jump=jump,
        )

        user_application_status_svc.create(
            obj_in=user_application_status, db=db_postgres,
        )

        return JSONResponse(
            status_code=200,
            content={'message': 'Status updated successfully'},
        )

    # Métodos específicos de cada estado
    async def assign_user(self, **kwargs):
        user_application_id = self.user_application.id
        user_to_assign_id = kwargs.get('user_to_assign_id')
        db_postgres = kwargs.get('db_postgres')
        jump = int(kwargs.get('jump', 0))

        user_application_user = UserApplicationUserCreate(
            user_application_id=user_application_id,
            user_id=user_to_assign_id,
        )

        user_application_user_svc.create(
            obj_in=user_application_user, db=db_postgres,
        )

        user_application_status = self.get_next_status(
            updated_by=kwargs.get('current_user').id,
            observation=kwargs.get('observation'),
            jump=jump,
        )

        user_application_status_svc.create(
            obj_in=user_application_status, db=db_postgres,
        )

        return JSONResponse(
            status_code=200,
            content={'message': 'User assigned successfully'},
        )

    async def send_to_academic_unit(self, **kwargs):
        db_postgres = kwargs.get('db_postgres')
        academic_unit_id = kwargs.get('academic_unit_id')
        jump = int(kwargs.get('jump', 0))

        user_application_academic_unit = UserApplicationAcademicUnitCreate(
            user_application_id=self.user_application.id,
            academic_unit_id=academic_unit_id,
        )

        user_application_academic_unit_svc.create(
            obj_in=user_application_academic_unit,
            db=db_postgres,
        )

        user_application_status = self.get_next_status(
            updated_by=kwargs.get('current_user').id,
            observation=kwargs.get('observation'),
            jump=jump,
        )

        user_application_status_svc.create(
            obj_in=user_application_status, db=db_postgres,
        )

        return JSONResponse(
            status_code=200,
            content={'message': 'Application sent to academic unit successfully'},
        )

    async def create_voting(self, **kwargs):
        # academic_unit_id = kwargs.get('academic_unit_id')
        db_postgres = kwargs.get('db_postgres')
        db_mongo = kwargs.get('db_mongo')
        jump = int(kwargs.get('jump', 0))

        user_id = self.user_application.user.id
        # user_app_acad_un = self.user_application.user_application_academic_units[0]
        # academic_unit_id = user_app_acad_un.academic_unit_id
        committee = user_rol_academic_unit_svc.get_student_committee(
            user_id=user_id, db=db_postgres,
        )

        obj_in: VotingCreate = VotingCreate(
            academic_unit_id=committee,
            user_application_id=self.user_application.id,
        )

        voting_create = voting_svc.create(obj_in=obj_in, db=db_postgres)

        voting_id = voting_create.id
        status = VotingStatus(
            result='PENDIENTE',
            date=datetime.now(),
            observation=None,
        )

        voting_info_to_create = VotingInfoCreate(
            id=voting_id,
            statuses=[status],
        )
        await voting_info_svc.create(
            obj_in=VotingInfo(**dict(voting_info_to_create)),
            db=db_mongo,
        )

        user_application_status = self.get_next_status(
            updated_by=kwargs.get('current_user').id,
            observation=kwargs.get('observation'),
            jump=jump,
        )

        user_application_status_svc.create(
            obj_in=user_application_status, db=db_postgres,
        )

        return JSONResponse(
            status_code=200,
            content={'message': 'Voting created successfully'},
        )

    async def send_to_school_council(self, **kwargs):
        db_postgres = kwargs.get('db_postgres')

        academic_unit_id = kwargs.pop('academic_unit_id', None)

        user_application_academic_unit = UserApplicationAcademicUnitCreate(
            user_application_id=self.user_application.id,
            academic_unit_id=academic_unit_id,
        )

        user_application_academic_unit_svc.create(
            obj_in=user_application_academic_unit,
            db=db_postgres,
        )

        await self.create_voting(academic_unit_id=academic_unit_id, **kwargs)

        return JSONResponse(
            status_code=200,
            content={
                'message':
                'Application sent to school council created successfully',
            },
        )

    async def close(self):
        """
        Finaliza la solicitud
        """

    async def reject(self, **kwargs):
        user_application_status = UserApplicationStatusCreate(
            user_application_id=self.user_application.id,
            status_id=REJECTED_STATUS_ID,
            updated_by=kwargs.get('current_user').id,
            observation=kwargs.get('observation'),
        )

        user_application_status_svc.create(
            obj_in=user_application_status, db=kwargs.get('db_postgres'),
        )

        return JSONResponse(
            status_code=200,
            content={'message': 'Application rejected successfully'},
        )
