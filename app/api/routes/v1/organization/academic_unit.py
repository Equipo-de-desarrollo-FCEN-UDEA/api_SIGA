from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.infraestructure.db.models.organization.academic_unit import AcademicUnit
from app.schemas.organization.academic_unit import AcademicUnitCreate, AcademicUnitInDB, AcademicUnitUpdate, School
from app.services.organization.academic_unit import academic_unit_svc
from app.api.routes.v1.utils.base_router import BaseRouter
from app.api.middleware.postgres_db import get_db


router = APIRouter()

BaseRouter(
    schem_in_db=AcademicUnitInDB,
    schem_create=AcademicUnitCreate,
    schem_update=AcademicUnitUpdate,
    service=academic_unit_svc,
    router=router,
    methods=["create", "get-all", "update"]
)


@router.get("/{id}", response_model=School, status_code=200)
def get_by_id(*, id: UUID, db_postgres:Session = Depends(get_db)) -> School:
    academic_unit = academic_unit_svc.get(id=id, db=db_postgres)
    if not academic_unit:
        return JSONResponse(status_code=404, content={"message": "Academic Unit not found"})
    return academic_unit