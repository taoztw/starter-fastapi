import asyncio

from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, select, Relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")
    # 删除了Team对应的heros也会被删除
    # heroes: list["Hero"] = Relationship(back_populates="team", cascade_delete=True)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

    team_id: int | None = Field(default=None, foreign_key="team.id")
    # 不使用python代码的时候，直接使用sql语句时候，删除team后，相关的hero也会被删除
    # team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="SET NULL")
    # team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="CASCADE")

    team: Team | None = Relationship(back_populates="heroes") # 其中包含另一个模型类中属性的名称。




sqlite_file_name = "hero.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"
async_engine = create_async_engine(sqlite_url, future=True, echo=True)
async_session = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    future=True,
)
# 创建表
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def main():
    await init_db()



async def create_team():
    team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
    team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
    async with async_session() as session:
        session.add(team_preventers)
        session.add(team_z_force)
        await session.commit()

async def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)


    async with async_session() as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)
        await session.commit()




async def select_heroes():
    async with async_session() as session:
        # statement = select(Hero).where(Hero.name == "Deadpond")
        # # statement = select(Hero).where(or_(Hero.age <= 35, Hero.age > 90))
        # heroes = await session.execute(statement)
        # for hero in heroes:
        #     print(hero)
        # statement = select(Hero).offset(3).limit(3)  # limit语法
        hero = await session.get(Hero, 1)  # 获取单行
        print(hero)

async def update_heros():
    async with async_session() as session:
        hero = await session.get(Hero, 1)
        hero.age = 100
        print(hero)
        session.add(hero)
        await session.commit()

async def delete_heros():
    async with async_session() as session:
        hero = await session.get(Hero, 1)
        await session.delete(hero)
        await session.commit()


# asyncio.run(main())
# asyncio.run(create_heroes())
# asyncio.run(select_heroes())
# asyncio.run(update_heros())
# asyncio.run(delete_heros())

asyncio.run(create_team())



# 表定义

class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
    is_training: bool = False

    team: "Team" = Relationship(back_populates="hero_links")
    hero: "Hero" = Relationship(back_populates="team_links")

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    hero_links: list[HeroTeamLink] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_links: list[HeroTeamLink] = Relationship(back_populates="hero")