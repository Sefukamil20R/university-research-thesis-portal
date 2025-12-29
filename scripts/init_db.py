"""
Database initialization script.
Creates initial roles and departments for the system.

Run this script once after setting up the database:
    python scripts/init_db.py
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.role import Role
from models.department import Department

# Create all tables
Base.metadata.create_all(bind=engine)


def init_roles(db: Session):
    """Initialize default roles with hierarchy levels"""
    roles = [
        {"role_name": "student", "hierarchy_level": 1},
        {"role_name": "advisor", "hierarchy_level": 2},
        {"role_name": "department_head", "hierarchy_level": 3},
        {"role_name": "admin", "hierarchy_level": 4},
    ]
    
    for role_data in roles:
        existing_role = db.query(Role).filter(Role.role_name == role_data["role_name"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.add(role)
            print(f"Created role: {role_data['role_name']}")
        else:
            print(f"Role already exists: {role_data['role_name']}")
    
    db.commit()


def init_departments(db: Session):
    """Initialize default departments"""
    departments = [
        {"name": "Computer Science", "code": "CS"},
        {"name": "Electrical Engineering", "code": "EE"},
        {"name": "Mathematics", "code": "MATH"},
        {"name": "Physics", "code": "PHYS"},
    ]
    
    for dept_data in departments:
        existing_dept = db.query(Department).filter(Department.code == dept_data["code"]).first()
        if not existing_dept:
            department = Department(**dept_data)
            db.add(department)
            print(f"Created department: {dept_data['name']} ({dept_data['code']})")
        else:
            print(f"Department already exists: {dept_data['name']}")
    
    db.commit()


def main():
    """Main initialization function"""
    db = SessionLocal()
    try:
        print("Initializing database...")
        init_roles(db)
        init_departments(db)
        print("Database initialization complete!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()

