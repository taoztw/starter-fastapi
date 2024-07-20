from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from exts.responses.json_response import (
    InternalErrorException,
    MethodnotallowedException,
    NotfoundException,
    LimiterResException,
    BadRequestException,
    ParameterException, UnauthorizedException,
)
from exts import logger

class ApiExceptionHandler:
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)

    def init_app(self, app: FastAPI):
        app.add_exception_handler(Exception, handler=self.all_exception_handler)
        app.add_exception_handler(
            StarletteHTTPException, handler=self.http_exception_handler
        )
        app.add_exception_handler(
            RequestValidationError, handler=self.validation_exception_handler
        )

    async def validation_exception_handler(
        self, request: Request, exc: RequestValidationError
    ):
        return ParameterException(
            http_status_code=400,
            message="参数校验错误",
            result={"detail": exc.errors(), "body": exc.body},
        )


    async def all_exception_handler(self, request: Request, exc: Exception):
        logger.debug(f"all_exception_handler: {exc}")
        return InternalErrorException()

    async def http_exception_handler(
        self, request: Request, exc: StarletteHTTPException
    ):
        if exc.status_code == 405:
            return MethodnotallowedException()
        if exc.status_code == 401:
            return UnauthorizedException()
        if exc.status_code == 404:
            return NotfoundException()
        elif exc.status_code == 429:
            return LimiterResException()
        elif exc.status_code == 500:
            return InternalErrorException()
        elif exc.status_code == 400:
            return BadRequestException(msg=exc.detail)
