from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any

from app.models.Order import Order
from app.models.User import User
from app.models.Product import Product
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

class OrderRequest(BaseModel):
    restaurant_id: int
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    order_id: int
    total_price: float
    status: str

@router.post("/orders", response_model=OrderResponse)
def place_order(order_request: OrderRequest, db: Session = Depends(get_sql_session)) -> Any:
    # Validate restaurant
    restaurant = db.query(User).filter(User.id == order_request.restaurant_id).first()
    if not restaurant or restaurant.user_type.__str__() != 'restaurant':
        raise HTTPException(status_code=400, detail="Invalid restaurant ID")

    # Validate product
    product = db.query(Product).filter(Product.id == order_request.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    # Calculate total price
    total_price = product.price * order_request.quantity

    # Create new order
    new_order = Order(
        restaurant_id=order_request.restaurant_id,
        product_id=order_request.product_id,
        quantity=order_request.quantity,
        total_price=total_price,
        status='pending'
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Return order confirmation
    return OrderResponse(
        order_id=new_order.id,
        total_price=new_order.total_price.__float__(),
        status=new_order.status.__str__()
    )
