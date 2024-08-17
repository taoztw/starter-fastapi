import asyncio
from asyncio import current_task
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncConnection,
    async_scoped_session,
)
import logging

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="session")
async def async_db_connection():
    # 初始化内存sql数据库
    async_engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    conn = await async_engine.connect()
    try:
        yield conn
    except:
        raise
    finally:
        await conn.rollback()

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await async_engine.dispose()


async def __session_within_transaction(
    async_db_connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_connection,
        class_=AsyncSession,
    )
    transaction = await async_db_connection.begin()

    yield async_scoped_session(async_session_maker, scopefunc=current_task)

    # no need to truncate, all data will be rolled back
    await transaction.rollback()


@pytest_asyncio.fixture(scope="function")
async def async_db_session(async_db_connection: AsyncConnection):
    async for session in __session_within_transaction(async_db_connection):
        # setup some data per function
        yield session


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=app, base_url="http://localhost:5571/starter/api/v1/learn"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
