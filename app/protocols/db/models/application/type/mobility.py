from datetime import datetime
from app.protocols.db.utils.link_model import LinkModel
from uuid import UUID

from enum import Enum

from app.protocols.db.utils.mongo_model import MongoModel

class MobilityType(Enum):
    NATIONAL_OUTGOING = "Saliente Nacional"
    INTERNATIONAL_OUTGOING = "Saliente Internacional"

class Process(Enum):
    RESEARCH_INTERSHIP = "Pasantía de Investigación"
    ACADEMIC_EXCHANGE = "Intercambio Académico"

class MobilityPurpose(Enum):
    DOUBLE_DEGREE = "Doble Titulación"
    RESEARCH_INTERSHIP = "Pasantía de Investigación"
    PROFESSIONAL_PRACTICE = "Práctica Profesional"
    ACADEMIC_EXCHANGE = "Intercambio Académico"

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
    date_start: datetime
    date_end: datetime
    total_time: int #tiempo total en meses
    date_report: datetime
    status: list[Status]
