from datetime import datetime
from typing import Annotated, Union

from fastapi import APIRouter, Depends, Response, responses
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
import sys

logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="Auth", level="INFO")


class AuthService:
    pass


class AuthApi:

    def __init__(self):
        self.router = APIRouter()
        self.auth_service = AuthService()

        self.router.add_api_route(path='/auth',
                                  endpoint=self.login_for_access_token,
                                  methods=['POST'])

        self.router.add_api_route(path='/health',
                                  endpoint=self.auth_health,
                                  methods=['GET'])

    async def login_for_access_token(self, auth_credentials: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Response:
        jwt = await self.auth_service.generate_user_jwt(
            user=auth_credentials.username,
            password=auth_credentials.password
        )
        return responses.JSONResponse(jwt, 200)

    async def auth_health(self, user_context: Annotated[dict, Depends(AuthService.get_auth_user_context)]):
        return responses.JSONResponse({
            "datetime": datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
            "status": "ok",
            "environment": CONFIG.ENVIRONMENT,
            'user': user_context['user']
        }, 200)