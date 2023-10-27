from app.generic import CrudApi
from loguru import logger
import sys
from structure.connectors import Base
from app.users import UserService
from structure.models import UserModel
from structure.schemas import UserSchema, UserInsert, UserUpdate
from typing import Any, Union, List

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
                           response_model=Union[schema, Any])

        self.user_service = UserService(model, schema)
