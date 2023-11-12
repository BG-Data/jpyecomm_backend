import os
# from infisical import InfisicalClient
from decouple import config
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))
from common.secrets import InfisicalClient 
from loguru import logger
import sys

logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="Config Settings", level="INFO")


class Config:

    ENVIRONMENT = config('ENVIRONMENT', default='test', cast=str)
    INFISICAL_TOKEN = config('INFISICAL_TOKEN')
    DATABASE_URL = config('DATABASE_URL', default='', cast=str) or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CRIPTOCODE = config("CRIPTOCODE", cast=str, default='teste')
    SECRET_KEY = config('SECRET_KEY', cast=str, default='teste')
    ALGORITHM = config('ALGORITHM', cast=str, default='HS256')
    DEV_PSWD = config('DEV_PSWD', cast=str, default='teste')
    MERCADO_PAGO_ACCESS_TOKEN = config('MERCADO_PAGO_ACCESS_TOKEN', cast=str, default='')
    PORT = config("PORT", default=5000, cast=int)
    UVICORN_WORKERS = config("UVICORN_WORKERS", default=1, cast=int)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=config('JWT_ACCESS_TOKEN_EXPIRES', default=1, cast=int))
    RELOAD = config('RELOAD', default=True, cast=bool)
    
    # def __init__(self):
    #     if self.INFISICAL_TOKEN and self.ENVIRONMENT != 'test':
    #         self.get_credentials()

    # def get_credentials(self):
    #     client = InfisicalClient(self.INFISICAL_TOKEN,
    #                              self.ENVIRONMENT)
    #     # client = InfisicalClient(token=config('INFISICAL_TOKEN'))
    #     # for secret in client.get_all_secrets(environment=ENVIRONMENT,
    #     #                                      path='/'):
    #     for secret_key, secret_value in client.get_secrets().items():
    #         if not hasattr(self, secret_key):
    #             setattr(self, secret_key, secret_value)
    #             logger.info(f'New secret add {secret_key}')


#OBS
# Sem acesso à AWS, a senha e usuário são teste e dev respectivamente (SQLITE)