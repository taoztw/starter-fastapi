import pathlib
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware
from config import settings
from exts.exceptions import ApiExceptionHandler
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
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
    docs_url=None,
    redoc_url=None,
    openapi_url=f"/{settings.PROJECT_ROOT_NAME}/openapi.json",
)

templates = Jinja2Templates(directory=f"{pathlib.Path.cwd()}/templates/")
staticfiles = StaticFiles(directory=f"{pathlib.Path.cwd()}/static")
app.mount(f"/{settings.PROJECT_ROOT_NAME}/static", staticfiles, name="static")


# 本地静态资源
@app.get(f"/{settings.PROJECT_ROOT_NAME}/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"/{settings.PROJECT_ROOT_NAME}/static/swagger-ui-bundle.js",
        swagger_css_url=f"/{settings.PROJECT_ROOT_NAME}/static/swagger-ui.css",
        swagger_favicon_url=f"/{settings.PROJECT_ROOT_NAME}/static/favicon.png",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    print(123)
    return get_swagger_ui_oauth2_redirect_html()


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
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
    # Access - Control - Allow - Origin
)


# 路由设置
app.include_router(api_router, prefix=f"/{settings.PROJECT_ROOT_NAME}/api/v1")
