from structure.models import UserModel
from structure.schemas import UserInsert
from common.generic import CrudService
from common import PasswordService
from datetime import date
from loguru import logger
import sys
from structure.connectors import Session, SessionLocal
from typing import List
from settings import Config

config = Config()

logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="BaseUser", level="INFO")


class BaseUsers(PasswordService, CrudService):
    def __init__(self,
                 model: UserModel = UserModel,
                 insert_schema: UserInsert = UserInsert):
        super().__init__(model, insert_schema)

    def __base_users_list(self) -> list:
        try:
            to_create = []
            dev = UserInsert(email='dev@ecomm.com',
                             name='dev',
                             password=self.hash_password(config.DEV_PSWD),
                             birthdate=date.today(),
                             lgpd=True,
                             document='',
                             document_type='',
                             user_type='admin'
                             )

            to_create.append(dev)
            return to_create
        except Exception as exp:
            logger.error(f'Error at base_users_list {exp}')
            raise exp

    def __check_base_users(self, session: Session) -> List[dict]:
        try:
            to_create = []
            for users in self.__base_users_list():
                result = session.query(UserModel).filter(UserModel.email == users.email).one_or_none()
                to_create.append({'insert': False if result else True,
                                  'schema': users})
            return to_create
        except Exception as exp:
            logger.error(f'Error at check_base_users {exp}')
            raise exp

    def create_base_users(self) -> dict:
        try:
            with SessionLocal() as session:

                created = 0
                for itens in self.__check_base_users(session):
                    if itens.get('insert') is True:
                        user_created = self.insert_item(itens.get('schema'),
                                                        session)
                        logger.info(f'user created: {user_created}')
                        created += 1
                return {'Users created': created}
        except Exception as exp:
            logger.error(f'Error at create_base_users {exp}')
            raise exp
        finally:
            session.close()
