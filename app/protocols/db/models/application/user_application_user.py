from __future__ import annotations

from uuid import UUID

from app.protocols.db.utils.link_model import LinkModel


class UserApplicationUser(LinkModel):
    user_application_id: UUID
    user_id: UUID
    is_active: bool
