from sqlalchemy import Column, Integer, String
from app.modassembly.database.sql.get_sql_session import Base

class RestaurantType(Base):
    __tablename__ = 'restaurant_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
