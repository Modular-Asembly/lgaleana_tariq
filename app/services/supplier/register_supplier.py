from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.models.Supplier import Supplier
from app.modassembly.database.sql.get_sql_session import get_sql_session
import bcrypt

# Define a Pydantic model for the supplier registration input
class SupplierCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Define a Pydantic model for the supplier registration output
class SupplierOut(BaseModel):
    id: int
    name: str
    email: EmailStr

# Create a FastAPI router
router = APIRouter()

@router.post("/suppliers/register", response_model=SupplierOut, status_code=status.HTTP_201_CREATED, summary="Register a new supplier")
def register_supplier(supplier: SupplierCreate, db: Session = Depends(get_sql_session)) -> SupplierOut:
    """
    Register a new supplier in the database.

    Args:
        supplier (SupplierCreate): The supplier registration details.
        db (Session): The database session.

    Returns:
        SupplierOut: The registered supplier details.
    """
    # Check if the email is already registered
    existing_supplier = db.query(Supplier).filter(Supplier.email == supplier.email).first()
    if existing_supplier:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash the password
    hashed_password = bcrypt.hashpw(supplier.password.encode('utf-8'), bcrypt.gensalt())

    # Create a new supplier instance
    new_supplier = Supplier(
        name=supplier.name,
        email=supplier.email,
        password_hash=hashed_password.decode('utf-8')
    )

    # Add the new supplier to the database
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    # Return the registered supplier details
    return SupplierOut(id=new_supplier.id.__int__(), name=new_supplier.name.__str__(), email=new_supplier.email.__str__())
