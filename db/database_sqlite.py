from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings

from contextlib import asynccontextmanager
from sqlalchemy.engine.url import URL
from config import settings

# 创建异步引擎对象

async_engine = create_async_engine(
    settings.SQLITE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
)

async_session = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    future=True,
)
