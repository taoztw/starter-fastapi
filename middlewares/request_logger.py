import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from exts import logger


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = uuid.uuid4().hex
        with logger.contextualize(request_id=request_id):
            try:
                response = await call_next(request)
            finally:
                pass
            return response
