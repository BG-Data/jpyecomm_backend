from fastapi import FastAPI
from api import UserApi #, ProductApi, SaleApi, AddressApi, PaymentApi
from structure.connectors import Base, engine

Base.metadata.create_all(bind=engine)


def init_app():
    app = FastAPI()
    api_routes = {'user':
                    {'router': UserApi(),
                    'tags': ['Usuarios'],
                    'prefix': '/user'}
                # 'product':
                #     {'router': ProductApi(),
                #     'tags': 'Produtos',
                #     'prefix': '/products'},
                # 'sale':
                #     {'router': SaleApi(),
                #     'tags': 'Vendas',
                #     'prefix': '/sales'},
                # 'address':
                #     {'router': AddressApi(),
                #     'tags': 'Endereços',
                #     'prefix': '/addresses'},
                # 'payment':
                #     {'router': PaymentApi(),
                #     'tags': 'Pagamentos',
                #     'prefix': '/payments'}
                }
    app = init_routes(app, api_routes)
    return app


def init_routes(app: FastAPI, api_routes: dict):
    for route_key in api_routes.keys():
        app.include_router(**api_routes.get(route_key))
    return app
