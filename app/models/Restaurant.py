from sqlalchemy import Column, Integer, String, ForeignKey
from app.modassembly.database.sql.get_sql_session import Base

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    restaurant_type_id = Column(Integer, ForeignKey('restaurant_types.id'), nullable=False)
