from sqlalchemy import Column, Integer, String
from app.modassembly.database.sql.get_sql_session import Base

class SupplierType(Base):
    __tablename__ = 'supplier_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
