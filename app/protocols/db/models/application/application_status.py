from __future__ import annotations

from uuid import UUID

from app.protocols.db.utils.link_model import LinkModel


class ApplicationStatus(LinkModel):
    application_id: UUID
    status_id: UUID
    step: int
