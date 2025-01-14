from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.Product import Product
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Define Pydantic models for input and output
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    supplier_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    id: int

class ProductDelete(BaseModel):
    id: int

class ProductResponse(BaseModel):
    message: str

# Create a FastAPI router
router = APIRouter()

@router.post("/product/manage", response_model=ProductResponse, summary="Manage a product")
def manage_product(
    action: str,
    product_data: Union[ProductCreate, ProductUpdate, ProductDelete],
    db: Session = Depends(get_sql_session)
) -> ProductResponse:
    """
    Manage a product by adding, updating, or removing it in the database.

    Args:
        action (str): The action to perform ('add', 'update', 'remove').
        product_data (Union[ProductCreate, ProductUpdate, ProductDelete]): The product data for the action.
        db (Session): The database session.

    Returns:
        ProductResponse: A confirmation message.
    """
    if action == 'add' and isinstance(product_data, ProductCreate):
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            supplier_id=product_data.supplier_id
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return ProductResponse(message=f"Product '{new_product.name.__str__()}' added successfully.")

    elif action == 'update' and isinstance(product_data, ProductUpdate):
        product = db.query(Product).filter(Product.id == product_data.id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        product.name = product_data.name
        product.description = product_data.description
        product.price = product_data.price
        product.supplier_id = product_data.supplier_id
        db.commit()
        return ProductResponse(message=f"Product '{product.name.__str__()}' updated successfully.")

    elif action == 'remove' and isinstance(product_data, ProductDelete):
        product = db.query(Product).filter(Product.id == product_data.id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        db.delete(product)
        db.commit()
        return ProductResponse(message=f"Product '{product.name.__str__()}' removed successfully.")

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action or data")

