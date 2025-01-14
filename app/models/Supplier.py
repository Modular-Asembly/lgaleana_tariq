from sqlalchemy import Column, Integer, String, ForeignKey
from app.modassembly.database.sql.get_sql_session import Base

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    supplier_type_id = Column(Integer, ForeignKey('supplier_types.id'), nullable=False)
