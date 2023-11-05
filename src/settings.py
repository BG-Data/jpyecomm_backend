import os
from decouple import config
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

# load_dotenv(os.path.join(basedir, '.env'))


class Config:
    PORT = config("PORT", default=5000, cast=int)
    UVICORN_WORKERS = config("UVICORN_WORKERS", default=1, cast=int)
    PSQL_USER = config("PSQL_USER", default='', cast=str)
    PSQL_PASSWORD = config("PSQL_PASSWORD", default='thisissecret', cast=str)
    PSQL_IP = config("PSQL_IP", default='localhost', cast=str)
    PSQL_DB = config("PSQL_DB", default='ecomm_of_love', cast=str)
    # postgresql+psycopg2://PSQL_USER:PSQL_PASSWORD@PSQL_IP/PSQL_DB
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='', cast=str) or 'sqlite:///' + os.path.join(basedir, 'sqlite.db')                                     
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CRIPTOCODE = config("CRIPTOCODE", cast=str)
    APPLICATION_NAME = 'Ecomm of love'
    RELOAD = config('RELOAD', default=True, cast=str)
    JWT_ACCESS_TOKEN_EXPIRES = config('JWT_ACCESS_TOKEN_EXPIRES', default=timedelta(hours=1))
    SECRET_KEY = config('SECRET_KEY', cast=str)
    ALGORITHM = config('ALGORITHM', cast=str)