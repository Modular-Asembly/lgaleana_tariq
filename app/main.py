from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers

from app.models.Product import Product
from app.models.Restaurant import Restaurant
from app.models.Supplier import Supplier
from app.models.Order import Order
from app.services.product.list_products import router
app.include_router(router)
from app.services.order.place_order import router
app.include_router(router)
from app.services.order.update_order_status import router
app.include_router(router)
from app.services.product.manage_product import router
app.include_router(router)
from app.services.restaurant.register_restaurant import router
app.include_router(router)
from app.services.supplier.register_supplier import router
app.include_router(router)

# Database

from app.modassembly.database.sql.get_sql_session import Base, engine
Base.metadata.create_all(engine)
