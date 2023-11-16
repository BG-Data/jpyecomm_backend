from common.generic import CrudApi
from common import PasswordService
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
from fastapi import HTTPException, status, Depends
from structure import MakeOptionalPydantic
from utils.exceptions import BadRequestException, UnauthorizedException, ForbiddenException, NotFoundException


logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="Api", level="INFO")

class UserApi(CrudApi):
    def __init__(self,
                 model: UserModel = UserModel,
                 schema: UserSchema = UserSchema,
                 insert_schema: UserInsert = UserInsert,
                 update_schema: UserUpdate = MakeOptionalPydantic.make_partial_model(UserUpdate),
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
        self.service = UserService(model, schema)
        self.password_service = PasswordService()

    def insert(self,
               insert_schema: UserInsert,
               session: Session = Depends(get_session)):
        try:
            insert_schema.password = self.password_service.hash_password(insert_schema.password)
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')

    def update(self,
               id: int,
               update_schema: MakeOptionalPydantic.make_partial_model(UserUpdate),
               session: Session = Depends(get_session)):
        
        if update_schema.model_dump(exclude_unset=True).get('old_password'):
            valid = self.password_service.get_password(update_schema.old_password,
                                                       self.crud.get_itens({'id': id}, session)[0].password)
            update_schema.old_password = None
            update_schema.password = self.password_service.hash_password(update_schema.password)
            if not valid:
                raise HTTPException(status_code=401, detail={
                    'status_code': status.HTTP_401_UNAUTHORIZED,
                    'info': 'The given password is not valid'})
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')


class ProductApi(CrudApi):
    def __init__(self,
                 model: ProductModel = ProductModel,
                 schema: ProductSchema = ProductSchema,
                 insert_schema: ProductInsert = ProductInsert,
                 update_schema: ProductUpdate = MakeOptionalPydantic.make_partial_model(ProductUpdate),
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
        # self.add_api_route('/caminho',
        #                    self.metodo_novo,
        #                    methods=['GET'],
        #                    response_model=dict)

        self.service = ProductService(model, schema)

    # def metodo_novo(self,
    #                 id: int,
    #                 session: Session = Depends(get_session)):
    #     try:
    #         resultado = session.query(ProductModel).all()
    #     except ValueError as exp:
    #         return f'Dado errado colocado aqui {exp}'
    #     except Exception as exp:
    #         logger.error(f" error do metodo novo: {exp}")

    def insert(self,
               insert_schema: ProductInsert,
               session: Session = Depends(get_session)):
    
        user = self.get_user_by_id(insert_schema.user_id)

        if user is None:
            raise UnauthorizedException(detail="Usuário não encontrado")
        
        if not (user == "vendedor" or user == "admin"):
            raise ForbiddenException(detail="Usuário não tem permissão para inserir produtos")
        
        try:
            return self.crud.insert_item(insert_schema, session)
        
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: MakeOptionalPydantic.make_partial_model(ProductUpdate),
               session: Session = Depends(get_session)):
        
        user = self.get_user_by_id(update_schema.user_id)

        if user is None:
            raise NotFoundException(detail="Usuário não encontrado. Impossível atualizar informações de produtos")
        
        if not (user == "vendedor" or user == "admin"): 
            raise ForbiddenException("Usuário não tem permissão para atualizar informações de produtos")
        
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')


class PaymentApi(CrudApi):
    def __init__(self,
                 model: PaymentMethodModel = PaymentMethodModel,
                 schema: PaymentSchema = PaymentSchema,
                 insert_schema: PaymentInsert = PaymentInsert,
                 update_schema: PaymentUpdate = MakeOptionalPydantic.make_partial_model(PaymentUpdate),
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

        self.service = PaymentService(model, schema)

    def insert(self,
               insert_schema: PaymentInsert,
               session: Session = Depends(get_session)):
        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: MakeOptionalPydantic.make_partial_model(PaymentUpdate),
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
                 update_schema: SaleUpdate = MakeOptionalPydantic.make_partial_model(SaleUpdate),
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

        self.service = SaleService(model, schema)

    def insert(self,
               insert_schema: SaleInsert,
               session: Session = Depends(get_session)):
        # TODO (André) -> Criar HttpException para o caso do usuário/produto/endereço/pagamento, etc não existir ou não for vendendor ou admin
        user = self.get_user_by_id(insert_schema.user_id)

        if user is None:
            raise NotFoundException()
        if not (user == "vendedor" or user == "admin"):
            raise ForbiddenException()

        # Verifica se o produto existe e tem permissão (exemplo)
        product = self.get_product_by_id(insert_schema.product_id)

        if product is None:
            raise NotFoundException(detail="Produto não encontrado")

        # TODO Verificar outras condições de permissão (endereço, pagamento, etc.)
        delivery_adress = self.get_delivery_adress_id(insert_schema.delivery_address_id)

        if delivery_adress is None:
            raise NotFoundException(detail="Endereço de entrega não encontrado")
        
        billing_adress = self.get_billing_adress_id(insert_schema.billing_address_id)

        if billing_adress is None:
            raise NotFoundException(detail="Endereço de cobrança não encontrado")
        
        payment_method = self.get_payment_method_id(insert_schema.payment_method_id)

        if payment_method is None:
            raise 

        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: MakeOptionalPydantic.make_partial_model(SaleUpdate),
               session: Session = Depends(get_session)):
        # TODO (André) -> Criar HttpException para o caso do usuário/produto/endereço/pagamento, etc não existir ou não for vendendor ou admin

        user = self.get_user_by_id(update_schema.user_id)

        if user is None:
            raise NotFoundException()
        if not (user == "vendedor" or user == "admin"):
            raise ForbiddenException()

        product = self.get_product_by_id(update_schema.product_id)

        if product is None:
            raise NotFoundException(detail="Produto não encontrado")

        delivery_adress = self.delivery_adress_id(update_schema.delivery_address_id)

        if delivery_adress is None:
            raise NotFoundException(detail="Endereço de entrega não encontrado")
        
        billing_adress = self.billing_adress_id(update_schema.billing_address_id)

        if billing_adress is None:
            raise NotFoundException(detail="Endereço de cobrança não encontrado")

        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')


class AddressApi(CrudApi):
    def __init__(self,
                 model: AddressModel = AddressModel,
                 schema: AddressSchema = AddressSchema,
                 insert_schema: AddressInsert = AddressInsert,
                 update_schema: AddressUpdate = MakeOptionalPydantic.make_partial_model(AddressUpdate),
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

        self.service = AddressService(model, schema)

    def insert(self,
               insert_schema: AddressInsert,
               session: Session = Depends(get_session)):
        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: MakeOptionalPydantic.make_partial_model(AddressUpdate),
               session: Session = Depends(get_session)):
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')
