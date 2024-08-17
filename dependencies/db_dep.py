from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

# from db.database import AsyncSessionLocal  # mysql
from db.database_sqlite import async_session  # sqlite


async def get_db_context() -> AsyncGenerator[AsyncSession, None]:

    session = async_session()
    try:
        yield session
        # await session.commit()  # 取消自动提交
    except SQLAlchemyError as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()
