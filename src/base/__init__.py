from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api import UserApi, ProductApi, SaleApi, AddressApi, PaymentApi, ProductFileApi
from structure.schemas import Health
from common.aws import AwsClient 
from settings import cfg
from common.auth import AuthApi, AuthService
from common.base_users import BaseUsers
from structure.connectors import Base, engine
from loguru import logger
import sys

logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="Init api", level="INFO")


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def init_app():
    app = FastAPI()
    api_routes = {'user':
                    {'router': UserApi(),
                        'tags': ['Usuarios'],
                        'prefix': '/user'},
                  'product':
                    {'router': ProductApi(),
                        'tags': ['Produtos'],
                        'prefix': '/products'},
                  'product_file':
                    {'router': ProductFileApi(),
                        'tags': ['Produtos e Arquivos'],
                        'prefix': '/products/files'},
                  'sale':
                    {'router': SaleApi(),
                        'tags': ['Vendas'],
                        'prefix': '/sales'},
                  'address':
                    {'router': AddressApi(),
                        'tags': ['Endereços'],
                        'prefix': '/addresses'},
                  'payment':
                    {'router': PaymentApi(),
                        'tags': ['Métodos de Pagamento'],
                        'prefix': '/payment_methods'}
                  }
    app = init_middlewares(app)
    app = init_auth(app)
    app = init_routes(app, api_routes)
    Base.metadata.create_all(bind=engine)
    base_users = BaseUsers().create_base_users()
    logger.info(base_users)
    return app, Base


def init_routes(app: FastAPI, api_routes: dict):

    @app.get('/', response_model=Health, status_code=200)
    def status_api():
        return Health().model_dump()

    for route_key in api_routes.keys():
        app.include_router(**api_routes.get(route_key))
    return app


def init_auth(app: FastAPI):
    app.include_router(
        AuthApi().router,
        tags=['Auth'],
    )
    return app
