from pydantic import BaseModel
from loguru import logger
import sys
from common import DatabaseSessions, get_current_method_name
from fastapi import HTTPException, Depends
from structure.connectors import Base
from sqlalchemy import or_
from structure.models import ProductFilesModel
from structure.connectors import Session, get_session


logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="Services", level="INFO")


class UserService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema


class ProductService(DatabaseSessions):
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema

    def get_product_urls(self, product_id: int,
                         session: Session = Depends(get_session)):
        try:
            result = session.query(ProductFilesModel)\
                            .filter(ProductFilesModel.product_id == product_id)
            return result
        except Exception as exp:
            logger.error(f'Error at >>>>> get_product urls {exp}')
            raise HTTPException(status_code=500, detail=str(exp))

    def delete_product_urls(self, product_id: int = None,
                            session: Session = Depends(get_session)):
        try:
            result = session.query(self.model)\
                            .filter(self.model.product_id == product_id).one()
            if result:
                logger.error('No item was found to be deleted')
                raise ValueError('Delete item not found')
            self.delete_session(session, result)
            logger.info('Row deleted')
            logger.info(f'{result.__tablename__} tabled deleted row with id {product_id}')
            return {'status': 'deleted',
                    "table":
                        {"name": result.__tablename__,
                         'id': result.id}
                    }
        except Exception as exp:
            logger.error(f'Error at >>>>> {get_current_method_name()}: {exp}')
            raise HTTPException(status_code=500, detail=str(exp))


class ProductFileService:
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
