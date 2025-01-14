from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.models.Restaurant import Restaurant
from app.modassembly.database.sql.get_sql_session import get_sql_session
import bcrypt

# Define a Pydantic model for the restaurant registration input
class RestaurantCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Define a Pydantic model for the registration confirmation output
class RestaurantOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Create a FastAPI router
router = APIRouter()

@router.post("/restaurants/register", response_model=RestaurantOut, summary="Register a new restaurant")
def register_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_sql_session)) -> RestaurantOut:
    """
    Register a new restaurant in the database.

    Args:
        restaurant (RestaurantCreate): The restaurant registration details.
        db (Session): The database session.

    Returns:
        RestaurantOut: The registered restaurant details.
    """
    # Check if the email is already registered
    existing_restaurant = db.query(Restaurant).filter(Restaurant.email == restaurant.email).first()
    if existing_restaurant:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = bcrypt.hashpw(restaurant.password.encode('utf-8'), bcrypt.gensalt())

    # Create a new restaurant instance
    new_restaurant = Restaurant(
        name=restaurant.name,
        email=restaurant.email,
        password_hash=hashed_password.decode('utf-8')
    )

    # Add the new restaurant to the database
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    # Return the registered restaurant details
    return RestaurantOut(
        id=new_restaurant.id.__int__(),
        name=new_restaurant.name.__str__(),
        email=new_restaurant.email.__str__()
    )
