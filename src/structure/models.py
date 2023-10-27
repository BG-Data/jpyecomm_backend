from structure.connectors import Base
from sqlalchemy import String, Sequence, Date, DateTime, Integer, Numeric, Column, Boolean
from pydantic import BaseModel


class ModelProduto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, Sequence('products_id', 1, 1),
                     primary_key=True, index=True)
    nome = Column(String(255),
                       index=True, nullable=False)


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('users_id', 1, 1),
                primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    birth_date = Column(Date, nullable=False, index=True)
    lgpd = Column(Boolean, nullable=False)
    document = Column(String(18), nullable=False, index=True)
    document_type = Column(String(10), nullable=False)
    user_type = Column(String, nullable=False)  # Comprador ou Vendedor

