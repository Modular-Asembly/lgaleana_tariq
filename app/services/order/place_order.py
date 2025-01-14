from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.Order import Order
from app.models.Product import Product
from app.models.Restaurant import Restaurant

router = APIRouter()

class OrderInput(BaseModel):
    restaurant_id: int
    product_id: int
    quantity: int

class OrderOutput(BaseModel):
    id: int
    restaurant_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str

    class Config:
        orm_mode = True

@router.post("/orders", response_model=OrderOutput, summary="Place a new order")
def place_order(order_input: OrderInput, db: Session = Depends(get_sql_session)) -> OrderOutput:
    """
    Place a new order in the database.

    Args:
        order_input (OrderInput): The input details for the order.
        db (Session): The database session.

    Returns:
        OrderOutput: The details of the placed order.
    """
    # Validate restaurant
    restaurant = db.query(Restaurant).filter(Restaurant.id == order_input.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Validate product
    product = db.query(Product).filter(Product.id == order_input.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Calculate total price
    total_price = product.price * order_input.quantity

    # Create new order
    new_order = Order(
        restaurant_id=order_input.restaurant_id,
        product_id=order_input.product_id,
        quantity=order_input.quantity,
        total_price=total_price,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return OrderOutput.from_orm(new_order)
