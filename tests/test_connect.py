import pytest
from db.database import AsyncSessionLocal


@pytest.mark.asyncio
async def test_db():
    db_session = AsyncSessionLocal()
    assert db_session is not None
