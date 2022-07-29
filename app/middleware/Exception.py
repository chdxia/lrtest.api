from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


class UnicornException(Exception):
    def __init__(self, code, errmeg, data=None):
        if data is None:
            data = {}
        self.code = code
        self.errmsg = errmeg
        self.data = data


async def unicorn_exception_handler(_: Request, exc: UnicornException):
    return JSONResponse(
        {
            "code": exc.code,
            "message": exc.errmsg,
            "data": exc.data
        }
    )


async def http_error_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        {
            "code": exc.status_code,
            "message": exc.detail,
            "data": exc.detail
        },
        status_code = exc.status_code,
        headers = exc.headers
    )


async def http422_error_handler(_: Request, exc: RequestValidationError | ValidationError):
    return JSONResponse(
        {
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "value error",
            "data": exc.errors()
        },
        status_code = 422
    )
