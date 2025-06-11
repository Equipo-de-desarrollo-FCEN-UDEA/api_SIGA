from __future__ import annotations

import asyncio
from datetime import datetime

from app.api.routes.v1.application.type.commission import advance_application_status
from app.core.celery_worker import celery_app
from app.core.logging import get_logger
from app.infraestructure.db.models.application import UserApplication
from app.infraestructure.db.models.application.user_application_status import (
    UserApplicationStatus,
)
from app.infraestructure.db.utils.mongo_session import engine as db_mongo
from app.infraestructure.db.utils.postgres_session import SessionLocal
from app.services.application.type.commission import commission_svc

log = get_logger(__name__)

COMMISSION_APP_ID = '190040d8-557e-4f41-92da-9916c1050e76'
COMMISSION_APPROVED_ID = '188ee606-f03f-4428-9301-8d7a4879d97b'


@celery_app.task(name='app.core.tasks.check_expired_commissions')
def check_expired_commissions():
    db_postgres = SessionLocal()
    today = datetime.now().date()

    try:
        # Obtiene todas las solicitudes activas de comisiones aprobadas
        user_applications = (
            db_postgres.query(UserApplication)
            .join(UserApplication.user_application_status)
            .filter(
                UserApplication.application_id == COMMISSION_APP_ID,
                UserApplicationStatus.status_id == COMMISSION_APPROVED_ID,
            )
            .all()
        )

        for user_application in user_applications:
            commission = commission_svc.get(id=user_application.id, db=db_mongo)
            if not commission:
                log.warning(
                    f'Commission not found for application {user_application.id}',
                )
                continue

            if commission.date_end.date() <= today:
                # Esta es la persona que hizo la solicitud
                current_user = user_application.user

                asyncio.run(
                    advance_application_status(
                        user_application_id=str(user_application.id),
                        request={},
                        is_approved=True,
                        db_mongo=db_mongo,
                        db_postgres=db_postgres,
                        current_user=current_user,
                    ),
                )

    except Exception as e:
        db_postgres.rollback()
        log.error(f'Error in check_expired_commissions: {e}')
    finally:
        db_postgres.close()
