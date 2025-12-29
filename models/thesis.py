"""
Thesis model for research document management.
Implements MAC (Mandatory Access Control) through classification levels.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class ThesisStatus(str, enum.Enum):
    """Thesis status enumeration"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class Thesis(Base):
    """
    Thesis model with classification levels for MAC.
    
    Classification levels (MAC):
    - 1 = Public
    - 2 = Internal
    - 3 = Confidential
    
    Only Admin can change classification level.
    """
    __tablename__ = "theses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    abstract = Column(Text, nullable=True)
    
    # MAC - Mandatory Access Control classification
    # Must match User clearance levels: 1=Public, 2=Internal, 3=Confidential
    classification_level = Column(Integer, default=1, nullable=False, index=True)
    
    # Status workflow
    status = Column(Enum(ThesisStatus), default=ThesisStatus.DRAFT, nullable=False)
    
    # Relationships
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    # File storage (path to file - TODO: Implement secure file storage)
    file_path = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    student = relationship("User", back_populates="theses")
    department = relationship("Department", back_populates="theses")

