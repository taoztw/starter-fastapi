from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from contextlib import asynccontextmanager
from sqlalchemy.engine.url import URL
from config import settings

# 创建异步引擎对象

async_engine = create_async_engine(
    url=URL.create(
        settings.ASYNC_DB_DRIVER,
        settings.DB_USER,
        settings.DB_PASSWORD,
        settings.DB_HOST,
        settings.DB_PORT,
        settings.DB_DATABASE,
    ),
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    future=False,
)
