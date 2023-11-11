import os
# from infisical import InfisicalClient
from decouple import config
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ENVIRONMENT = config('ENVIRONMENT', default='test', cast=str)

    # if config('INFISICAL_TOKEN'):
    #     client = InfisicalClient(token=config('INFISICAL_TOKEN'))
    #     for secret in client.get_all_secrets(environment=ENVIRONMENT,
    #                                          path='/'):
    #         exec(f"{secret.secret_name} = '{secret.secret_value}'")
    # else:
    PORT = config("PORT", default=5000, cast=int)
    UVICORN_WORKERS = config("UVICORN_WORKERS", default=1, cast=int)
    DATABASE_URL = config('DATABASE_URL', default='', cast=str) or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CRIPTOCODE = config("CRIPTOCODE", cast=str, default='teste')
    RELOAD = config('RELOAD', default=True, cast=str)
    JWT_ACCESS_TOKEN_EXPIRES = config('JWT_ACCESS_TOKEN_EXPIRES', default=1)
    SECRET_KEY = config('SECRET_KEY', cast=str, default='teste')
    ALGORITHM = config('ALGORITHM', cast=str, default='HS256')
    DEV_PSWD = config('DEV_PSWD', cast=str, default='teste')
    MERCADO_PAGO_ACCESS_TOKEN = config('MERCADO_PAGO_ACCESS_TOKEN', cast=str, default='')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(JWT_ACCESS_TOKEN_EXPIRES))
    
#OBS
# Sem acesso à AWS, a senha e usuário são teste e dev respectivamente (SQLITE)