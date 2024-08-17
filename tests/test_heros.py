import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from models.hero import Hero

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio


async def test_get_hero(async_db_session: AsyncSession, async_client: AsyncClient):
    response = await async_client.get(url="/heros?offset=0&limit=1")
    assert response.status_code == 200


async def test_create_hero_sql(async_db_session: AsyncSession):
    db_hero = Hero(name="Deadpond", secret_name="Dive Wilson")
    async_db_session.add(db_hero)
    await async_db_session.commit()
    await async_db_session.refresh(db_hero)
    logger.info(db_hero)
    assert db_hero.id is not None
