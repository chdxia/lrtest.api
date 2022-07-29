from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


class UvicornException(Exception):
    def __init__(self, code, errmeg, data=None):
        if data is None:
            data = {}
        self.code = code
        self.errmsg = errmeg
        self.data = data


# 重写uvicorn异常
async def uvicorn_exception_handler(_: Request, exc: UvicornException):
    return JSONResponse(
        {
            "code": exc.code,
            "message": exc.errmsg,
            "data": exc.data
        }
    )


# 重写HTTPException
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


# 重写422异常
async def http422_error_handler(_: Request, exc: RequestValidationError | ValidationError):
    return JSONResponse(
        {
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "value error",
            "data": exc.errors()
        },
        status_code = 422
    )
