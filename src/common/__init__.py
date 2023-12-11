from sqlalchemy.orm import Session
import cryptocode
from settings import config
import inspect


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


def get_current_method_name() -> str:
    # Get the current frame
    frame = inspect.currentframe()

    # Go up one level in the stack to get the caller's frame
    caller_frame = inspect.getouterframes(frame, 2)[1]

    # Extract the name of the calling function
    caller_method_name = caller_frame.function

    # Print the name of the calling function
    return caller_method_name


def generate_variables_dict(func, kwargs: dict) -> dict:
    variables = {}
    for key, value in inspect.signature(func).parameters.items():
        locals()[key] = kwargs.get(key)
        if locals()[key] is not None:
            locals()[key] = value.annotation(locals()[key])
        variables.update({key: locals()[key]})
    return variables