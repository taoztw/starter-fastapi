import pathlib
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from config import settings
from db.redis_client import RedisCli
from exts.exceptions import ApiExceptionHandler
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from exts.requestvar import BindContextvarMiddleware
from middlewares.request_logger import RequestLoggerMiddleware
from db.redis_client import RedisClient
from router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisClient.init_redis_connect()
    yield
    await RedisClient.close_redis_connect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    description="FastAPI Template",
    version="0.0.1",
    debug=True if settings.PROJECT_ENV == "LOCAL" else False,
)

templates = Jinja2Templates(directory=f"{pathlib.Path.cwd()}/templates/")
staticfiles = StaticFiles(directory=f"{pathlib.Path.cwd()}/static")
app.mount("/static", staticfiles, name="static")


# 本地静态资源
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.png",
    )


# 注册全局异常
ApiExceptionHandler().init_app(app)
app.add_middleware(BindContextvarMiddleware)
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://10.1.6.35",
        "http://10.1.6.35:3000",
        "http://localhost",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
    # Access - Control - Allow - Origin
)


# 路由设置
app.include_router(api_router, prefix="/starter/api/v1")

