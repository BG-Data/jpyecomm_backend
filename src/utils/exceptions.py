from fastapi import HTTPException

class BadRequestException(HTTPException):
    def __init__(self, detail=None, status_code=400, *args, **kwargs):
        if detail is None:
            detail = "Erro 400: Bad Request"
        else:
            detail = detail
        super().__init__(detail, status_code, *args, **kwargs)


class UnauthorizedException(HTTPException):
    def __init__(self, detail=None, status_code=401, *args, **kwargs):
        if detail is None:
            detail = "Erro 401: Unauthorized"
        else:
            detail = detail
        super().__init__(detail, status_code, *args, **kwargs)

class ForbiddenException(HTTPException):
    def __init__(self, detail=None, status_code=403, *args, **kwargs):
        if detail is None:
            detail = "Err0 403: Forbidden"
        else:
            detail = detail
        super().__init__(detail, status_code, *args, **kwargs)

class NotFoundException(HTTPException):
    def __init__(self, detail=None, status_code=404, *args, **kwargs):
        if detail is None:
            detail = "Erro 404: Not Found"
        else:
            detail = detail
        super().__init__(detail, status_code, *args, **kwargs)

class MethodNotAllowedException(HTTPException):
    def __init__(self, detail=None, status_code=405, *args, **kwargs):
        if detail is None:
            detail = "Erro 405: Method Not Allowed"
        else:
            detail = detail
        super().__init__(detail, status_code, *args, **kwargs)

class ServerErrorException(HTTPException):
    def __init__(self, detail=None, status_code=500, *args, **kwargs):
        if detail is None:
            detail = "Erro 500: Internal Server Error"
        else:
            detail = detail
        super().__init__(detail, status_code)

class BadGatewayException(HTTPException):
    def __init__(self, detail=None, status_code=502, *args, **kwargs):
        if detail is None:
            detail = "Erro 502: Bad Gateway"
        else:
            detail = detail
        super().__init__(detail, status_code)
