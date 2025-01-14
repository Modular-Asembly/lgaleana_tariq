from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.Product import Product
from app.modassembly.database.sql.get_sql_session import get_sql_session
from pydantic import BaseModel

# Define a Pydantic model for the product output
class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    supplier_id: int

    class Config:
        orm_mode = True

# Create a FastAPI router
router = APIRouter()

@router.get("/products", response_model=List[ProductOut], summary="List all products")
def list_products(db: Session = Depends(get_sql_session)) -> List[ProductOut]:
    """
    Retrieve all products from the database and return them as a list.

    Returns:
        List[ProductOut]: A list of products.
    """
    products = db.query(Product).all()
    return [ProductOut.from_orm(product) for product in products]
