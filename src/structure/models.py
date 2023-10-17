from structure.connectors import Base
from sqlalchemy import String, Sequence, Date, DateTime, Integer, Numeric, Column
from pydantic import BaseModel


class ModelProduto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, Sequence('products_id', 1, 1),
                     primary_key=True, index=True)
    nome = Column(String(255),
                       index=True, nullable=False)
