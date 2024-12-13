from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.protocols.db.models.application.type.mobility import MobilityPurpose
from app.protocols.db.models.application.type.mobility import MobilityType
from app.protocols.db.models.application.type.mobility import Process
from app.schemas.application.user_application import UserApplicationStatus


class Subject(BaseModel):
    extern_code: str
    extern_name: str
    intern_code: str
    intern_name: str


class MobilityBase(BaseModel):
    id: UUID | None = None
    process: Process
    type: MobilityType
    purpose: MobilityPurpose
    destination_country: str
    destination_institution: str
    academic_program: str
    name_contact_person: str
    cellphone_contact_person: str
    email_contact_person: str
    date_start: datetime
    date_end: datetime
    subjects: list[Subject] | None = []
    total_time: int  # tiempo total en meses
    date_report: datetime
    status: list[UserApplicationStatus] | None = []


class MobilityCreate(MobilityBase):
    pass


class MobilityUpdate(BaseModel):
    process: Process | None = None
    type: MobilityType | None = None
    purpose: MobilityPurpose | None = None
    destination_country: str | None = None
    destination_institution: str | None = None
    academic_program: str | None = None
    name_contact_person: str | None = None
    cellphone_contact_person: str | None = None
    email_contact_person: str | None = None
    date_start: datetime | None = None
    date_end: datetime | None = None
    total_time: int | None = None
    date_report: datetime | None = None
    subjects: list[Subject] | None = None



class Mobility(MobilityBase):
    pass
