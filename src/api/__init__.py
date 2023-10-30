from common.generic import CrudApi, Depends
from loguru import logger
import sys
from structure.connectors import Session, get_session
from app import UserService, ProductService, AddressService, \
    SaleService, PaymentService
from structure.models import UserModel, ProductModel, AddressModel, \
    SaleModel, PaymentMethodModel
from structure.schemas import UserSchema, UserInsert, UserUpdate, \
    ProductSchema, ProductInsert, ProductUpdate, AddressSchema, \
    AddressInsert, AddressUpdate, SaleSchema, SaleUpdate, \
    SaleInsert, PaymentSchema, PaymentUpdate, PaymentInsert
from typing import Any, Union, List, Dict


logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="Api", level="INFO")


class UserApi(CrudApi):
    def __init__(self,
                 model: UserModel = UserModel,
                 schema: UserSchema = UserSchema,
                 insert_schema: UserInsert = UserInsert,
                 update_schema: UserUpdate = UserUpdate,
                 *args, **kwargs):
        super().__init__(model, schema, insert_schema, update_schema,
                         *args, **kwargs)
        self.add_api_route('/',
                           self.get,
                           methods=['GET'],
                           response_model=Union[List[schema],
                                                schema, Any])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]])

        self.user_service = UserService(model, schema)

    def insert(self,
               insert_schema: UserInsert,
               session: Session = Depends(get_session)):
        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: UserUpdate,
               session: Session = Depends(get_session)):
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')


class ProductApi(CrudApi):
    def __init__(self,
                 model: ProductModel = ProductModel,
                 schema: ProductSchema = ProductSchema,
                 insert_schema: ProductInsert = ProductInsert,
                 update_schema: ProductUpdate = ProductUpdate,
                 *args, **kwargs):
        super().__init__(model, schema, insert_schema, update_schema,
                         *args, **kwargs)
        self.add_api_route('/',
                           self.get,
                           methods=['GET'],
                           response_model=Union[List[schema],
                                                schema, Any])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]])

        self.user_service = ProductService(model, schema)

    def insert(self,
               insert_schema: ProductInsert,
               session: Session = Depends(get_session)):
        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: ProductUpdate,
               session: Session = Depends(get_session)):
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')

class PaymentApi(CrudApi):
    def __init__(self,
                 model: PaymentMethodModel = PaymentMethodModel,
                 schema: PaymentSchema = PaymentSchema,
                 insert_schema: PaymentInsert = PaymentInsert,
                 update_schema: PaymentUpdate = PaymentUpdate,
                 *args, **kwargs):
        super().__init__(model, schema, insert_schema, update_schema,
                         *args, **kwargs)
        self.add_api_route('/',
                           self.get,
                           methods=['GET'],
                           response_model=Union[List[schema],
                                                schema, Any])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]])

        self.user_service = PaymentService(model, schema)

    def insert(self,
               insert_schema: ProductInsert,
               session: Session = Depends(get_session)):
        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: ProductUpdate,
               session: Session = Depends(get_session)):
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')

class SaleApi(CrudApi):
    def __init__(self,
                 model: SaleModel = SaleModel,
                 schema: SaleSchema = SaleSchema,
                 insert_schema: SaleInsert = SaleInsert,
                 update_schema: SaleUpdate = SaleUpdate,
                 *args, **kwargs):
        super().__init__(model, schema, insert_schema, update_schema,
                         *args, **kwargs)
        self.add_api_route('/',
                           self.get,
                           methods=['GET'],
                           response_model=Union[List[schema],
                                                schema, Any])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]])

        self.user_service = SaleService(model, schema)

    def insert(self,
               insert_schema: ProductInsert,
               session: Session = Depends(get_session)):
        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: ProductUpdate,
               session: Session = Depends(get_session)):
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')

class AddressApi(CrudApi):
    def __init__(self,
                 model: AddressModel = AddressModel,
                 schema: AddressSchema = AddressSchema,
                 insert_schema: AddressInsert = AddressInsert,
                 update_schema: AddressUpdate = AddressUpdate,
                 *args, **kwargs):
        super().__init__(model, schema, insert_schema, update_schema,
                         *args, **kwargs)
        self.add_api_route('/',
                           self.get,
                           methods=['GET'],
                           response_model=Union[List[schema],
                                                schema, Any])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]])

        self.user_service = AddressService(model, schema)

    def insert(self,
               insert_schema: ProductInsert,
               session: Session = Depends(get_session)):
        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: ProductUpdate,
               session: Session = Depends(get_session)):
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')


