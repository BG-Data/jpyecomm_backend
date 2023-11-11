import os
from infisical import InfisicalClient
from decouple import config
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ENVIRONMENT = config('ENVIRONMENT', default='test', cast=str)

    if config('INFISICAL_TOKEN'):
        client = InfisicalClient(token=config('INFISICAL_TOKEN'))
        client.get_all_secrets(environment=ENVIRONMENT,
                               path='/')
    PORT = config("PORT", default=5000, cast=int)
    UVICORN_WORKERS = config("UVICORN_WORKERS", default=1, cast=int)
    PSQL_USER = config("PSQL_USER", default='', cast=str)
    PSQL_PASSWORD = config("PSQL_PASSWORD", default='thisissecret', cast=str)
    PSQL_IP = config("PSQL_IP", default='localhost', cast=str)
    PSQL_DB = config("PSQL_DB", default='ecomm_of_love', cast=str)
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='', cast=str) or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CRIPTOCODE = config("CRIPTOCODE", cast=str, default='teste')
    APPLICATION_NAME = 'Ecomm of love'
    RELOAD = config('RELOAD', default=True, cast=str)
    JWT_ACCESS_TOKEN_EXPIRES = config('JWT_ACCESS_TOKEN_EXPIRES', default=timedelta(hours=1))
    SECRET_KEY = config('SECRET_KEY', cast=str, default='teste')
    ALGORITHM = config('ALGORITHM', cast=str, default='HS256')
    DEV_PSWD = config('DEV_PSWD', cast=str, default='teste')
    MERCADO_PAGO_ACCESS_TOKEN = config('MERCADO_PAGO_ACCESS_TOKEN', cast=str, default='')

#OBS
# Sem acesso à AWS, a senha e usuário são teste e dev respectivamente (SQLITE)