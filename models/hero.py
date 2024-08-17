import asyncio

from sqlmodel import Field, SQLModel, select, Relationship


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None)

    team_id: int | None = Field(default=None, foreign_key="team.id")


class HeroCreate(HeroBase):
    password: str
    pass


class HeroPublic(HeroBase):
    id: int


class HeroUpdate(HeroBase):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: str | None = None


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list["Hero"] = Relationship(
        back_populates="team", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    hashed_password: str | None = Field(None)
    team: Team | None = Relationship(
        back_populates="heroes", sa_relationship_kwargs={"lazy": "selectin"}
    )


class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None


if __name__ == "__main__":
    from db.database_sqlite import async_engine, async_session

    async def drop_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    async def init_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    asyncio.run(drop_tables())
    asyncio.run(init_db())

    # 创建一些hero数据
    async def create_heroes():
        hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
        hero_2 = Hero(name="Spider", secret_name="Peter Parker")
        async with async_session() as session:
            session.add(hero_1)
            session.add(hero_2)
            await session.commit()

    asyncio.run(create_heroes())
