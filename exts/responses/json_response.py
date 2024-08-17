from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import time
import json
import datetime
import decimal
import typing
from sqlalchemy.ext.declarative import DeclarativeMeta


class ApiResponse(JSONResponse):
    http_status_code = 200
    result: Optional[Dict[str, Any]] = None
    message = "成功响应"
    timestamp = int(time.time() * 1000)

    def __init__(self, http_status_code=None, result=None, message=None, **options):
        self.message = message or self.message
        self.http_status_code = http_status_code or self.http_status_code
        self.result = result or self.result

        # 返回内容体
        body = dict(
            message=self.message,
            result=self.result,
            timestamp=self.timestamp,
        )
        super(ApiResponse, self).__init__(
            status_code=self.http_status_code, content=body, **options
        )

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


class BadRequestException(ApiResponse):
    http_status_code = 400
    result = None
    message = "Bad Request"


class EmptyUserException(ApiResponse):
    http_status_code = 400
    result = None
    message = "请输入用户名和密码"


class LimiterResException(ApiResponse):
    http_status_code = 429
    result = None  # 结果可以是{} 或 []
    message = "访问的速度过快"


class ParameterException(ApiResponse):
    http_status_code = 400
    result = {}
    message = "参数校验错误,请检查提交的参数信息"


class UnauthorizedException(ApiResponse):
    http_status_code = 401
    result = {}
    message = "invalid authorization credentials"


class ForbiddenException(ApiResponse):
    http_status_code = 403
    result = {}
    message = "失败！当前访问没有权限，或操作的数据没权限!"


class NotfoundException(ApiResponse):
    http_status_code = 404
    result = {}
    message = "访问地址不存在"


class MethodnotallowedException(ApiResponse):
    http_status_code = 405
    result = {}
    message = "不允许使用此方法提交访问"


class OtherException(ApiResponse):
    http_status_code = 800
    result = {}
    message = "未知的其他HTTPEOOER异常"


class InternalErrorException(ApiResponse):
    http_status_code = 500
    result = {}
    message = "Server unkonwn error"


class InvalidTokenException(ApiResponse):
    http_status_code = 401
    message = "很久没操作，令牌失效"


class ExpiredTokenException(ApiResponse):
    http_status_code = 401
    message = "很久没操作，令牌过期"
    success = False


class FileTooLargeException(ApiResponse):
    http_status_code = 413
    result = None  # 结果可以是{} 或 []
    message = "文件体积过大"


class FileTooManyException(ApiResponse):
    http_status_code = 413
    message = "文件数量过多"
    result = None  # 结果可以是{} 或 []


class FileExtensionException(ApiResponse):
    http_status_code = 401
    message = "文件扩展名不符合规范"
    result = None  # 结果可以是{} 或 []


class Success(ApiResponse):
    http_status_code = 200
    message = "获取成功"


class Businesserror(ApiResponse):
    http_status_code = 200
    result = None  # 结果可以是{} 或 []
    message = "业务错误逻辑处理"


class Fail(ApiResponse):
    http_status_code = 500
    result = None  # 结果可以是{} 或 []
    message = "操作失败"
