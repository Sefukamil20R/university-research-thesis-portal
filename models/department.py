"""
Department model for organizing users and theses.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Department(Base):
    """
    Department model for organizing users and research.
    """
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relationships
    users = relationship("User", back_populates="department")
    theses = relationship("Thesis", back_populates="department")

