from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class SchemaProduto(BaseModel):
    id: int
    nome: str


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str


class UserSchema(UserBase):
    id: int
    name: str
    password: str
    birth_date: date
    lgpd: bool
    document: str
    document_type: str
    user_type: str


class UserGet(UserBase):
    name: str
    birth_date: date
    lgpd: bool
    document: str
    document_type: str
    user_type: str


class UserInsert(UserBase):
    name: str
    password: str
    birth_date: date
    lgpd: bool
    document: str
    document_type: str
    user_type: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    password: Optional[str] = None
    birth_date: Optional[date] = None
    lgpd: Optional[bool] = None
    document: Optional[str] = None
    document_type: Optional[str] = None
    user_type: Optional[str] = None

