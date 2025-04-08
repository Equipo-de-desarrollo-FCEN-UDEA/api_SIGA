from __future__ import annotations

from uuid import UUID

from app.protocols.db.utils.link_model import LinkModel


class UserApplicationStatus(LinkModel):
    user_application_id: UUID
    status_id: UUID
    updated_by: UUID
    observation: str
