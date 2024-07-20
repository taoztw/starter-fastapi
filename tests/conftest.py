from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from config import get_settings
from typing import AsyncGenerator

from db.database import AsyncSessionLocal
from app import app


# auto use会作用于每一条用例
@pytest.fixture(scope="session", autouse=True)
async def db():
    db_session = AsyncSessionLocal()
    yield db_session
    await db_session.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

