from __future__ import annotations

from datetime import datetime
from typing import Protocol
from uuid import UUID


class MongoModel(Protocol):
    id: UUID
    created_at: datetime
    updated_at: datetime
