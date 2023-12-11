from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal
from settings import config
# Usuários
from utils.enums import UserType


class PydanticModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # @validator('*', pre=True)
    # def format_date_fields(cls, v):
    #     if isinstance(v, date):
    #         return v.strftime('%d-%m-%Y')
    #     elif isinstance(v, datetime):
    #         return v.strftime('%d-%m-%Y %H:%M:%S')
    #     return v


class Health(PydanticModel):
    datetime: str = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
    status: str = 'ok'
    environment: str = config.ENVIRONMENT


class UserBase(PydanticModel):
    email: str


class UserSchema(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    password: str
    birthdate: date
    lgpd: bool
    document: str
    document_type: str
    user_type: UserType
    deleted: bool


class UserInsert(UserBase):
    name: str
    password: str
    birthdate: date
    lgpd: bool
    document: str
    document_type: str
    user_type: UserType
    deleted: bool = False


class UserUpdate(UserInsert):
    old_password: str


class ProductBase(PydanticModel):
    name: str
    product_type: str
    quantity: int
    unit_value: Decimal
    labor_time: Decimal
    obs: str


class ProductSchema(ProductBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    infos: str
    category: bool
    details: str
    personalized_name: str
    personalized_type: str
    url = List[Optional[str]] = []


class ProductInsert(ProductBase):
    infos: str
    user_id: int
    category: bool
    details: str
    personalized_name: str
    personalized_type: str


class ProductUpdate(ProductBase):
    infos: str
    user_id: int
    category: bool
    details: str
    personalized_name: str
    personalized_type: str


class ProductFileBase(PydanticModel):
    filename: str
    content_type: str
    file: str


class ProductFileSchema(ProductFileBase):
    id: int
    product_id: int


class ProductFileInsert(ProductFileBase):
    product_id: int
    file: Optional[str]  # url


class ProductFileUrls(PydanticModel):
    file: Optional[str]


class ProductFileUpdate(ProductFileInsert):
    pass

# Address


class AddressBase(PydanticModel):
    postal_code: str
    street: str
    number: str
    neighborhood: str
    state: str
    country: str


class AddressSchema(AddressBase):
    id: int
    created_at: datetime
    updated_at: datetime
    complement: str
    reference_point: str
    address_type: str
    delivery: bool
    billing: bool
    user_id: int


class AddressInsert(AddressBase):
    complement: str
    reference_point: str
    address_type: str
    delivery: bool
    billing: bool
    user_id: int


class AddressUpdate(AddressInsert):
    pass


# Payments


class PaymentBase(PydanticModel):
    name: str


class PaymentSchema(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    payment_type: str
    user_id: int


class PaymentInsert(PaymentBase):
    payment_type: str
    user_id: int


class PaymentUpdate(PaymentInsert):
    pass


# Sales


class SaleBase(PydanticModel):
    total_value: Decimal
    unit_value: Decimal
    quantity: int
    shipping_cost: Decimal


class SaleSchema(SaleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    currency_type: str
    shipping_time: int
    delivery_type: str
    payment_platform: str
    shipping_type: str  # corrente, util, etc
    order_status: str
    order_notes: Optional[str] = None
    return_reason: Optional[str] = None
    print_name: Optional[str] = None
    gift_message: Optional[str] = None
    product_id: int
    payment_method_id: int
    buyer_id: int
    delivery_address_id: int
    billing_address_id: int


class SaleInsert(SaleBase):
    currency_type: str
    shipping_time: int
    delivery_type: str
    payment_platform: str
    shipping_type: str  # corrente, util, etc
    order_status: str
    order_notes: Optional[str] = None
    return_reason: Optional[str] = None
    print_name: Optional[str] = None
    gift_message: Optional[str] = None
    product_id: int
    payment_method_id: int
    buyer_id: int
    delivery_address_id: int
    billing_address_id: int


class SaleUpdate(SaleInsert):
    pass



