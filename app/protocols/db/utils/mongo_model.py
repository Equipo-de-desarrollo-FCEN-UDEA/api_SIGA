from typing import Protocol
from datetime import datetime
from uuid import UUID

class MongoModel(Protocol):
    id_postgres: UUID
    created_at: datetime
    updated_at: datetime