"""
Thesis router - CRUD operations for research theses.
Implements RBAC and MAC access controls.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from models.thesis import Thesis
from models.role import Role
from auth.dependencies import get_current_active_user
from auth.rbac import require_role, require_minimum_role
from auth.mac import require_clearance
from schemas.thesis import ThesisCreate, ThesisResponse, ThesisUpdate

router = APIRouter(prefix="/thesis", tags=["Thesis"])


@router.post("/", response_model=ThesisResponse, status_code=status.HTTP_201_CREATED)
async def create_thesis(
    thesis_data: ThesisCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new thesis (Student role only).
    
    RBAC: Requires Student role
    MAC: Classification level must be <= user's clearance level
    """
    # RBAC: Only students can create theses
    user_role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not user_role or user_role.role_name.lower() != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can create theses"
        )
    
    # MAC: User cannot create thesis with classification above their clearance
    if thesis_data.classification_level > current_user.clearance_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot create thesis with classification level {thesis_data.classification_level}. "
                   f"Your clearance level: {current_user.clearance_level}"
        )
    
    new_thesis = Thesis(
        title=thesis_data.title,
        abstract=thesis_data.abstract,
        classification_level=thesis_data.classification_level,
        student_id=current_user.id,
        department_id=thesis_data.department_id
    )
    
    db.add(new_thesis)
    db.commit()
    db.refresh(new_thesis)
    
    return new_thesis


@router.get("/", response_model=List[ThesisResponse])
async def list_theses(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List theses accessible to the user.
    
    MAC: Users can only see theses at or below their clearance level.
    """
    # MAC: Filter by clearance level
    theses = db.query(Thesis).filter(
        Thesis.classification_level <= current_user.clearance_level
    ).all()
    
    return theses


@router.get("/{thesis_id}", response_model=ThesisResponse)
async def get_thesis(
    thesis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific thesis by ID.
    
    MAC: User must have clearance level >= thesis classification level.
    """
    thesis = db.query(Thesis).filter(Thesis.id == thesis_id).first()
    
    if not thesis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thesis not found"
        )
    
    # MAC: Check clearance level
    if thesis.classification_level > current_user.clearance_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Insufficient clearance level."
        )
    
    return thesis


@router.put("/{thesis_id}", response_model=ThesisResponse)
async def update_thesis(
    thesis_id: int,
    thesis_update: ThesisUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a thesis.
    
    RBAC: Only Admin can change classification level
    MAC: Users can only update theses they own or have permission for
    """
    thesis = db.query(Thesis).filter(Thesis.id == thesis_id).first()
    
    if not thesis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thesis not found"
        )
    
    # MAC: Check clearance level
    if thesis.classification_level > current_user.clearance_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Insufficient clearance level."
        )
    
    user_role = db.query(Role).filter(Role.id == current_user.role_id).first()
    
    # RBAC: Only admin can change classification level
    if thesis_update.classification_level is not None:
        if not user_role or user_role.role_name.lower() != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin can change classification level"
            )
        
        # MAC: New classification must be <= admin's clearance level
        if thesis_update.classification_level > current_user.clearance_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot set classification level above your clearance level"
            )
    
    # RBAC: Only thesis owner or admin/reviewer can update
    if thesis.student_id != current_user.id:
        if not user_role or user_role.hierarchy_level < 2:  # Advisor level or above
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own theses"
            )
    
    # Update fields
    if thesis_update.title is not None:
        thesis.title = thesis_update.title
    if thesis_update.abstract is not None:
        thesis.abstract = thesis_update.abstract
    if thesis_update.classification_level is not None:
        thesis.classification_level = thesis_update.classification_level
    if thesis_update.status is not None:
        thesis.status = thesis_update.status
    
    db.commit()
    db.refresh(thesis)
    
    return thesis


@router.delete("/{thesis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thesis(
    thesis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a thesis (Admin only).
    
    RBAC: Requires Admin role
    """
    thesis = db.query(Thesis).filter(Thesis.id == thesis_id).first()
    
    if not thesis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thesis not found"
        )
    
    user_role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not user_role or user_role.role_name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete theses"
        )
    
    db.delete(thesis)
    db.commit()
    
    return None

