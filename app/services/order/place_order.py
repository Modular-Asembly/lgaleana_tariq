from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.Product import Product
from app.models.Restaurant import Restaurant
from app.models.Order import Order
from app.models.RestaurantType import RestaurantType
from app.models.SupplierType import SupplierType
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Define Pydantic models for input and output
class OrderCreate(BaseModel):
    restaurant_id: int
    product_id: int
    quantity: int

class OrderConfirmation(BaseModel):
    order_id: int
    message: str

# Create a FastAPI router
router = APIRouter()

@router.post("/orders/place", response_model=OrderConfirmation, summary="Place a new order")
def place_order(order_data: OrderCreate, db: Session = Depends(get_sql_session)) -> OrderConfirmation:
    """
    Place a new order in the database if the restaurant and supplier types are compatible.

    Args:
        order_data (OrderCreate): The order details including restaurant ID, product ID, and quantity.
        db (Session): The database session.

    Returns:
        OrderConfirmation: Confirmation of the placed order.
    """
    # Retrieve the restaurant and product from the database
    restaurant = db.query(Restaurant).filter(Restaurant.id == order_data.restaurant_id).first()
    product = db.query(Product).filter(Product.id == order_data.product_id).first()

    # Validate order details
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if order_data.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than zero")

    # Check compatibility between restaurant and supplier types
    restaurant_type = db.query(RestaurantType).filter(RestaurantType.id == restaurant.restaurant_type_id).first()
    supplier_type = db.query(SupplierType).filter(SupplierType.id == product.supplier_id).first()

    if not restaurant_type or not supplier_type or restaurant_type.id != supplier_type.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incompatible restaurant and supplier types")

    # Calculate total price
    total_price = product.price * order_data.quantity

    # Create a new order
    new_order = Order(
        restaurant_id=restaurant.id.__int__(),
        product_id=product.id.__int__(),
        quantity=order_data.quantity,
        total_price=total_price,
        status="pending"
    )

    # Add the new order to the database
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Return order confirmation
    return OrderConfirmation(order_id=new_order.id.__int__(), message="Order placed successfully")
