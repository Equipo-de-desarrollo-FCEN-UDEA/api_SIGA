from __future__ import annotations

from datetime import datetime
from enum import Enum

from app.protocols.db.utils.link_model import LinkModel
from app.protocols.db.utils.mongo_model import MongoModel


class MobilityType(Enum):
    NATIONAL_OUTGOING = 'Saliente Nacional'
    INTERNATIONAL_OUTGOING = 'Saliente Internacional'


class Process(Enum):
    RESEARCH_INTERSHIP = 'Pasantía de Investigación'
    ACADEMIC_EXCHANGE = 'Intercambio Académico'


class MobilityPurpose(Enum):
    DOUBLE_DEGREE = 'Doble Titulación'
    RESEARCH_INTERSHIP = 'Pasantía de Investigación'
    PROFESSIONAL_PRACTICE = 'Práctica Profesional'
    ACADEMIC_EXCHANGE = 'Intercambio Académico'


class Subject:
    extern_code: str
    extern_name: str
    intern_code: str
    intern_name: str


class Status(LinkModel):
    name: str
    updated_by: str
    date: datetime


class Mobility(MongoModel):
    proccess: Process
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
    total_time: int  # tiempo total en meses
    date_report: datetime
    subjects: list[Subject]
    status: list[Status]
