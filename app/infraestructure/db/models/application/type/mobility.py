from __future__ import annotations

from datetime import datetime
from uuid import UUID

from odmantic import Field
from odmantic import Model

from app.schemas.application.type.mobility import Subject
from app.schemas.application.user_application import UserApplicationStatus


class Mobility(Model):
    id: UUID = Field(primary_field=True)
    process: str
    type: str
    purpose: str
    destination_country: str
    destination_institution: str
    academic_program: str
    name_contact_person: str
    cellphone_contact_person: str
    email_contact_person: str
    date_start: datetime
    date_end: datetime
    total_time: int
    date_report: datetime = Field(default_factory=datetime.utcnow)
    subjects: list[Subject]
    status: list[UserApplicationStatus]
