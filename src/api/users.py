from app.generic import CrudApi, Depends
from loguru import logger
import sys
from structure.connectors import Session, get_session
from app.users import UserService
from structure.models import UserModel
from structure.schemas import UserSchema, UserInsert, UserUpdate
from typing import Any, Union, List, Dict


logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="UserApi", level="INFO")


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
            logger.error(f'error at insert user {exp}')
    
    def update(self,
               id: int,
               update_schema: UserUpdate,
               session: Session = Depends(get_session)):
        try:
            return self.crud.update_item(id, update_schema, session)
        except Exception as exp:
            logger.error(f'error at insert user {exp}')