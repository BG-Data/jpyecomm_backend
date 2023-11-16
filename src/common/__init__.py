from sqlalchemy.orm import Session
import cryptocode
from settings import Config

config = Config()


class DatabaseSessions:

    def create_session(self, db: Session, db_action):
        try:
            db.add(db_action)
            db.commit()
            db.refresh(db_action)
            return db_action
        except Exception as e:
            db.rollback()
            raise e

    def update_session(self, db: Session, db_action):
        try:
            db.commit()
            db.flush()
            return db_action
        except Exception as e:
            db.rollback()
            raise e
    
    def delete_session(self, db: Session, db_action):
        try:
            db.delete(db_action)
            db.commit()
            return db_action
        except Exception as e:
            db.rollback()
            raise e
        

class PasswordService:
    criptocode = config.CRIPTOCODE

    # def set_password(self):
    #     pass

    @classmethod
    def get_password(cls, plain_password: str, hashed_password: str) -> bool:
        '''
        Checks if the password is compatible with the password hash.

            Args:
                plain_password (string): fetch the user insert forms password to be evaluated
                hashed_password (string): hashed password fetched by the DB engine.

            Returns:
                boolean type -> True for correct or False for incorrect plain_password inserted          

            Raises:
                TypeError: If any of the args is not str or the return is not boolean.
        '''
        return cryptocode.decrypt(hashed_password, cls.criptocode) == plain_password

    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        '''
        get the password hash.

            Args:
                plain_password (string): create a hashed password

            Returns:
                string type -> plain password added

            Raises:
                TypeError: If any of the args is not string or the return is not string.
        '''
        return cryptocode.encrypt(plain_password, cls.criptocode)
