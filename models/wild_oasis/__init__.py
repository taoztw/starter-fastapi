from models.wild_oasis.bookings import Bookings
from models.wild_oasis.guests import Guests
from models.wild_oasis.cabins import Cabins
from models.wild_oasis.settings import Settings


if __name__ == "__main__":
    from db.database_sqlite import async_engine, async_session
    from sqlmodel import SQLModel
    import asyncio

    async def drop_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    async def init_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    asyncio.run(drop_tables())
    asyncio.run(init_db())
