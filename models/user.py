from db.base_class import Base
from sqlmodel import SQLModel, Field
import uuid


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str | None = Field(default=None)
    refresh_token: str | None = Field(default=None)


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    pass


class UserEmailCode(UserBase):
    code: str


class UserResetPassword(SQLModel):
    reset_token: str


if __name__ == "__main__":
    from db.database_sqlite import async_engine, async_session
    import asyncio

    async def drop_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    async def init_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    asyncio.run(drop_tables())
    asyncio.run(init_db())
