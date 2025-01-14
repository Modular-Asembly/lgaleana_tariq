from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.Order import Order
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Define a Pydantic model for the input
class OrderStatusUpdate(BaseModel):
    order_id: int
    new_status: str

# Define a Pydantic model for the output
class OrderStatusUpdateResponse(BaseModel):
    order_id: int
    status: str
    message: str

# Create a FastAPI router
router = APIRouter()

@router.put("/orders/status", response_model=OrderStatusUpdateResponse, summary="Update order status")
def update_order_status(update_request: OrderStatusUpdate, db: Session = Depends(get_sql_session)) -> OrderStatusUpdateResponse:
    """
    Update the status of an order in the database.

    Args:
        update_request (OrderStatusUpdate): The request containing the order ID and new status.
        db (Session): The database session.

    Returns:
        OrderStatusUpdateResponse: Confirmation of the order status update.
    """
    # Retrieve the order from the database
    order = db.query(Order).filter(Order.id == update_request.order_id).first()

    # If the order does not exist, raise an HTTP 404 error
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update the order status
    order.status = update_request.new_status
    db.commit()
    db.refresh(order)

    # Return a confirmation message
    return OrderStatusUpdateResponse(
        order_id=order.id.__int__(),
        status=order.status.__str__(),
        message="Order status updated successfully"
    )
