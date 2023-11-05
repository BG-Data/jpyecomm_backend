from fastapi import FastAPI, Depends
from api import UserApi, ProductApi, SaleApi, AddressApi, PaymentApi
from common.auth import AuthApi, AuthService
from structure.connectors import Base, engine


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
    app = init_auth(app)
    app = init_routes(app, api_routes)
    Base.metadata.create_all(bind=engine)
    return app


def init_routes(app: FastAPI, api_routes: dict):
    for route_key in api_routes.keys():
        # if route_key != 'user':
        app.include_router(**api_routes.get(route_key),
                            dependencies=[Depends(AuthService.get_auth_user_context)])
        # else:
        #     app.include_router(**api_routes.get(route_key))
    return app


def init_auth(app: FastAPI):
    app.include_router(
        AuthApi().router,
        tags=['Auth'],
    )
    return app
