from common.generic import CrudApi, Depends
from common import PasswordService
from loguru import logger
import sys
from structure.connectors import Session, get_session
from app import UserService, ProductService, AddressService, \
    SaleService, PaymentService, ProductFileService
from structure.models import UserModel, ProductModel, AddressModel, \
    SaleModel, PaymentMethodModel, ProductFilesModel
from structure.schemas import UserSchema, UserInsert, UserUpdate, \
    ProductSchema, ProductInsert, ProductUpdate, AddressSchema, \
    AddressInsert, AddressUpdate, SaleSchema, SaleUpdate, \
    SaleInsert, PaymentSchema, PaymentUpdate, PaymentInsert, \
    ProductFileInsert, ProductFileSchema, ProductFileUpdate, \
    UserInsertAdmin
from typing import Any, Union, List, Dict
from fastapi import HTTPException, status, UploadFile, Request
from fastapi.responses import Response
from structure import MakeOptionalPydantic
from common.auth import AuthService
from uuid import uuid4
from json import dumps 


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
                                                schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any])
        self.add_api_route('/privileged',
                           self.insert_privileged,
                           methods=['POST'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.service = UserService(model, schema)
        self.password_service = PasswordService()

    def get(self, user_id: int = None, limit: int = 10, offset: int = 0,
            get_schema: Request = None, session: Session = Depends(get_session)):
        try:
            user_data = super().get(user_id, limit, offset, get_schema, session)
            return [user.model_dump(exclude={'password'}) for user in user_data]
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')

    def insert_privileged(self, insert_schema: UserInsertAdmin,
                          session: Session = Depends(get_session),
                          token: str = Depends(AuthService.oauth2_scheme)):
        'This user is restricted for admin creation only'
        try:
            if AuthService.get_auth_user_context(token).get('type') == 'admin':
                insert_schema.password = self.password_service.hash_password(insert_schema.password)
                return super().insert(insert_schema, session).model_dump(exclude={'password'})
            else:
                raise HTTPException(status_code=401, detail={
                    'status_code': status.HTTP_401_UNAUTHORIZED,
                    'info': 'The given user type is not allowed'})
        except Exception as exp:
            logger.error(f'error at insert privileged {self.__class__.__name__} {exp}')

    def insert(self,
               insert_schema: UserInsert,
               session: Session = Depends(get_session)):
        'Ordinary user -> buyer'
        try:
            insert_schema.password = self.password_service.hash_password(insert_schema.password)
            return super().insert(insert_schema, session).model_dump(exclude={'password'})
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
            return self.crud.update_item(id, update_schema, session).model_dump(exclude={'password'})
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')


class ProductFileApi(CrudApi):
    def __init__(self,
                 model: ProductFilesModel = ProductFilesModel,
                 schema: ProductFileSchema = ProductFileSchema,
                 insert_schema: ProductFileInsert = ProductFileInsert,
                 update_schema: ProductFileUpdate = MakeOptionalPydantic.make_partial_model(ProductFileUpdate),
                 *args, **kwargs):
        super().__init__(model, schema, insert_schema, update_schema,
                         *args, **kwargs)

        self.add_api_route('/',
                           self.get,
                           methods=['GET'],
                           response_model=Union[List[schema],
                                                schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[List[schema],
                                                schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]],
                           dependencies=[Depends(AuthService.get_auth_user_context)])

        self.service = ProductFileService(model, schema)

    async def insert(self,
                     files: List[UploadFile],
                     product_id: int,
                     session: Session = Depends(get_session)):
        try:
            inserted_files = []
            for insertion in files:
                filename = insertion.filename if insertion.filename else str(uuid4())
                result = await self.service.create_product_image_url(insertion, filename, product_id)
                insert_schema = self.insert_schema(product_id=product_id,
                                                   file=result.get('url'),
                                                   filename=filename,
                                                   content_type=insertion.content_type)
                inserted_files.append(self.crud.insert_item(insert_schema, session).model_dump())
            return inserted_files
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
            raise HTTPException(status_code=500, detail=f'Error at insert file {exp}')

    async def delete(self,
                     id: int,
                     session: Session = Depends(get_session)):
        try:
            url_deleted = self.service.delete_product_url(id, session)
            file_deleted = super().delete(id, session=session)
            if file_deleted == []:
                return Response(content="No product file found to delete ",
                                status_code=200)
            return Response(content=dumps({"bucket_deleted": url_deleted,
                                           "db_deleted": file_deleted}),
                            status_code=200)
        except Exception as exp:
            logger.error(f'error at delete {self.__class__.__name__} {exp}')
            raise HTTPException(status_code=500, detail=f'Error at deleted file {exp}')


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
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]],
                           dependencies=[Depends(AuthService.get_auth_user_context)])

        self.service = ProductService(model, schema)

    def get(self, id: int = None,
            limit: int = 5,
            offset: int = 0,
            get_schema: Request = None,
            session: Session = Depends(get_session)):
        try:
            products = []
            results = super().get(id, limit, offset, get_schema, session)
            if results == []:
                return Response(content="No product found",
                                status_code=200)

            for result in results:
                urls = self.service.get_product_urls(result.id, session)
                result.urls = urls
                products.append(result.model_dump())

            return products

        except Exception as exp:
            logger.error(f'error at get {self.__class__.__name__} {exp}')
            raise HTTPException(status_code=500, detail=f'Error at get_product {exp}')

    def insert(self,
               insert_schema: ProductInsert,
               session: Session = Depends(get_session)):
        try:
            result = self.crud.insert_item(insert_schema, session)
            return result
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
            raise HTTPException(status_code=500, detail=f'Error at get insert product {exp}')

    def update(self,
               id: int,
               update_schema: MakeOptionalPydantic.make_partial_model(ProductUpdate),
               session: Session = Depends(get_session)):
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at update {self.__class__.__name__} {exp}')
            raise HTTPException(status_code=500, detail=f'Error at get update product {exp}')

    def delete(self, id: int = None,
               session: Session = Depends(get_session)):
        try:
            url_deleted = self.service.delete_product_urls(id, session)
            product_deleted = super().delete(id, session)
            if product_deleted == []:
                return Response(content="No product found to delete ",
                                status_code=200)
            return Response(content=dumps({"bucket_deleted": url_deleted,
                                           "db_deleted": product_deleted}),
                            status_code=200)

        except Exception as exp:
            logger.error(f'error at get {self.__class__.__name__} {exp}')
            raise HTTPException(status_code=500, detail=f'Error at get_product {exp}')


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
                                                schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]],
                           dependencies=[Depends(AuthService.get_auth_user_context)])

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
                                                schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]],
                           dependencies=[Depends(AuthService.get_auth_user_context)])

        self.service = SaleService(model, schema)

    def insert(self,
               insert_schema: SaleInsert,
               session: Session = Depends(get_session)):
        # TODO (André) -> Criar HttpException para o caso do usuário/produto/endereço/pagamento, etc não existir ou não for vendendor ou admin 

        try:
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'error at insert {self.__class__.__name__} {exp}')
    
    def update(self,
               id: int,
               update_schema: MakeOptionalPydantic.make_partial_model(SaleUpdate),
               session: Session = Depends(get_session)):
        # TODO (André) -> Criar HttpException para o caso do usuário/produto/endereço/pagamento, etc não existir ou não for vendendor ou admin 

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
                                                schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.insert,
                           methods=['POST'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.update,
                           methods=['PUT'],
                           response_model=Union[schema, Any],
                           dependencies=[Depends(AuthService.get_auth_user_context)])
        self.add_api_route('/',
                           self.delete,
                           methods=['DELETE'],
                           response_model=Union[schema, Any, Dict[str, str]],
                           dependencies=[Depends(AuthService.get_auth_user_context)])

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
