from app.infraestructure.db.utils.base import Base

#SERVICES
from app.services.users.user import user_svc
from app.services.users.rol import rol_svc
from app.services.users.user_rol_academic_unit import user_rol_academic_unit_svc
from app.services.users.type.student import student_svc
from app.services.users.type.professor import professor_svc
from app.services.users.type.administrative import administrative_svc
from app.services.organization.academic_unit_type import academic_unit_type_svc
from app.services.organization.academic_unit import academic_unit_svc
#application services
from app.services.application.application import application_svc
from app.services.application.user_application import user_application_svc
from app.services.application.user_application_academic_unit import user_application_academic_unit_svc
#application types
from app.services.application.type.mobility import mobility_svc

#VOTING
from app.services.voting.voting import voting_svc
from app.services.voting.vote import vote_svc
from app.services.voting.vote_type import vote_type_svc
from app.services.voting.voting_info import voting_info_svc



# CRUD
from app.infraestructure.db.crud.users.user import user_crud
from app.infraestructure.db.crud.users.rol import rol_crud
from app.infraestructure.db.crud.users.user_rol_academic_unit import user_rol_academic_unit_crud
#student crud
from app.infraestructure.db.crud.users.type.student import student_crud
from app.infraestructure.db.crud.users.type.professor import professor_crud
from app.infraestructure.db.crud.users.type.administrative import administrative_crud
#organization crud
from app.infraestructure.db.crud.organization.academic_unit_type import academic_unit_type_crud
from app.infraestructure.db.crud.organization.academic_unit import academic_unit_crud
#application crud
from app.infraestructure.db.crud.application.application import application_crud
from app.infraestructure.db.crud.application.user_application import user_application_crud
from app.infraestructure.db.crud.application.user_application_academic_unit import user_application_academic_unit_crud
#application types
from app.infraestructure.db.crud.application.type.mobility import mobility_crud

#VOTING
from app.infraestructure.db.crud.voting.voting import voting_crud
from app.infraestructure.db.crud.voting.vote import vote_crud
from app.infraestructure.db.crud.voting.vote_type import vote_type_crud
from app.infraestructure.db.crud.voting.voting_info import voting_info_crud

from sqlalchemy import event
from app.core.logging import get_logger

log = get_logger(__name__)

#En este archivo lo que hacemos en crear la session en la base de datos

def init_db() -> None:

    user_svc.register_observer(user_crud)
    rol_svc.register_observer(rol_crud)
    user_rol_academic_unit_svc.register_observer(user_rol_academic_unit_crud)
    academic_unit_type_svc.register_observer(academic_unit_type_crud)
    academic_unit_svc.register_observer(academic_unit_crud)
    student_svc.register_observer(student_crud)
    professor_svc.register_observer(professor_crud)
    administrative_svc.register_observer(administrative_crud)

    #application config
    application_svc.register_observer(application_crud)
    user_application_svc.register_observer(user_application_crud)
    user_application_academic_unit_svc.register_observer(user_application_academic_unit_crud)
    #application types config
    mobility_svc.register_observer(mobility_crud)

    #voting config
    voting_svc.register_observer(voting_crud)
    vote_svc.register_observer(vote_crud)
    vote_type_svc.register_observer(vote_type_crud)
    voting_info_svc.register_observer(voting_info_crud)