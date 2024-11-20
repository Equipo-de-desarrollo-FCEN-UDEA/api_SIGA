from sqlalchemy import Column, Uuid, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.infraestructure.db.utils.base_model import BaseModel

class Voting(BaseModel):  
    academic_unit_id = Column(Uuid, ForeignKey("academic_unit.id"), nullable=False)
    user_application_id = Column(Uuid, ForeignKey("user_application.id"), nullable=False)

    # relations
    academic_unit = relationship("AcademicUnit", back_populates="votings", lazy="joined")
    user_application = relationship("UserApplication", back_populates="votings", lazy="joined")
    votes = relationship("Vote", back_populates="voting", lazy="joined")