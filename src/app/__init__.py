from pydantic import BaseModel
from loguru import logger
import sys
from structure.connectors import Base


logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="Services", level="INFO")


class UserService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema


class ProductService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema

class PaymentService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema

class SaleService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema

class AddressService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema
