from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from decimal import Decimal
# Usuários


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str


class UserSchema(UserBase):
    id: int
    nome: str
    senha: str
    dt_nasc: date
    lgpd: bool
    documento: str
    tipo_documento: str
    tipo_usuario: str
    deletado: bool


class UserInsert(UserBase):
    nome: str
    senha: str
    dt_nasc: date
    lgpd: bool
    documento: str
    tipo_documento: str
    tipo_usuario: str
    deletado: bool = False


class UserUpdate(UserBase):
    email: Optional[str] = None
    nome: Optional[str] = None
    senha: Optional[str] = None
    dt_nasc: Optional[date] = None
    lgpd: Optional[bool] = None
    documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    tipo_usuario: Optional[str] = None
    deletado: Optional[bool] = None
# Produtos


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome: str
    tipo_produto: str
    quantidade: int
    valor_unitario: Decimal
    tempo_fabrica: Decimal
    observacao: str


class ProductSchema(ProductBase):
    id: int
    infos: str
    categoria: bool
    detalhes: str
    url_imagens: str
    nome_personalizado: str
    tipo_personalizado: str


class ProductInsert(ProductBase):
    infos: str
    categoria: bool
    detalhes: str
    url_imagens: str
    nome_personalizado: str
    tipo_personalizado: str


class ProductUpdate(ProductBase):
    infos: Optional[str] = None
    categoria: Optional[bool] = None
    detalhes: Optional[str] = None
    url_imagens: Optional[str] = None
    nome_personalizado: Optional[str] = None
    tipo_personalizado: Optional[str] = None
