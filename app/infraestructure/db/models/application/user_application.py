from sqlalchemy import Column, Uuid, ForeignKey
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel

class UserApplication(BaseModel):
    user_id = Column(Uuid, ForeignKey("user.id"), nullable=False)
    application_id = Column(Uuid, ForeignKey("application.id"), nullable=False)

    # relations
    user = relationship("User", back_populates="user_applications", lazy="joined")
    application = relationship("Application", back_populates="user_applications", lazy="joined")
    user_application_academic_units = relationship("UserApplicationAcademicUnit", back_populates="user_application")
    votings = relationship("Voting", back_populates="user_application")