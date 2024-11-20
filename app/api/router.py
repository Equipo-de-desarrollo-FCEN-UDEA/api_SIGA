from fastapi import APIRouter

from app.api.routes import ping
from app.api.routes.v1.users import user
from app.api.routes.v1.users import rol
from app.api.routes.v1.users import user_rol_academic_rol
from app.api.routes.v1.users.type import student
from app.api.routes.v1.users.type import professor
from app.api.routes.v1.users.type import administrative

from app.api.routes.v1.organization import academic_unit_type
from app.api.routes.v1.organization import academic_unit

from app.api.routes.v1.users import auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(ping.router, tags=["ping"])

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(rol.router, prefix="/rol", tags=["rol"])
api_router.include_router(user_rol_academic_rol.router, prefix="/user_rol_academic_unit", tags=["user_rol_academic_unit"])
api_router.include_router(student.router, prefix="/student", tags=["student"])
api_router.include_router(professor.router, prefix="/professor", tags=["professor"])
api_router.include_router(administrative.router, prefix="/administrative", tags=["administrative"])


api_router.include_router(academic_unit_type.router, prefix="/academic_unit_type", tags=["academic_unit_type"])
api_router.include_router(academic_unit.router, prefix="/academic_unit", tags=["academic_unit"])

#voting
from app.api.routes.v1.voting import voting
from app.api.routes.v1.voting import vote_type
from app.api.routes.v1.voting import vote
api_router.include_router(voting.router, prefix="/voting", tags=["voting"])
api_router.include_router(vote_type.router, prefix="/vote_type", tags=["vote_type"])
api_router.include_router(vote.router, prefix="/vote", tags=["vote"])


#application
from app.api.routes.v1.application import application
from app.api.routes.v1.application.type import mobility

api_router.include_router(application.router, prefix="/application", tags=["application"])
api_router.include_router(mobility.router, prefix="/mobility", tags=["mobility"])
