from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.database_sqlite import async_session
from dependencies import get_db_context
from exts.responses.json_response import Success
from models.hero import (
    Hero,
    HeroPublic,
    HeroBase,
    HeroCreate,
    HeroUpdate,
    Team,
    TeamCreate,
    TeamUpdate,
    TeamPublic,
    HeroPublicWithTeam,
)

router = APIRouter()


@router.post("/heros", response_model=HeroPublic)
async def create_hero(
    hero: HeroCreate, db_session: AsyncSession = Depends(get_db_context)
):
    extra_data = {"hashed_password": hero.password}
    db_hero = Hero.model_validate(hero, update=extra_data)
    db_session.add(db_hero)
    await db_session.commit()
    await db_session.refresh(db_hero)

    return db_hero


# 原生写法
# @router.get("/heros", response_model=list[Hero])
# async def read_hearos():
#     async with async_session() as session:
#         heros = await session.execute(select(Hero))
#         heros = heros.scalars().all()
#         return heros


# @router.get("/heros", response_model=list[HeroBase])
# async def read_hearos(db_session: AsyncSession = Depends(get_db_context)):
#     heros = await db_session.execute(select(Hero))
#     heros = heros.scalars().all()
#     return heros


@router.get("/heros/{hero_id}", response_model=HeroPublicWithTeam)
async def read_hero(hero_id: int, db_session: AsyncSession = Depends(get_db_context)):
    hero = await db_session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.get("/heros", response_model=list[HeroPublic])
async def read_heroes(
    offset: int = 0,
    limit: int = Query(default=1, le=100),
    db_session: AsyncSession = Depends(get_db_context),
):
    heroes = await db_session.execute(select(Hero).offset(offset).limit(limit))
    heroes = heroes.scalars().all()
    return heroes


@router.patch("/heros/{hero_id}", response_model=HeroPublic)
async def update_hero(
    hero_id: int, hero: HeroUpdate, db_session: AsyncSession = Depends(get_db_context)
):
    db_hero = await db_session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in hero_data:
        hashed_password = "test"
        extra_data["hashed_password"] = hashed_password
    db_hero.sqlmodel_update(hero_data, update=extra_data)
    db_session.add(db_hero)
    await db_session.commit()
    await db_session.refresh(db_hero)

    return db_hero


@router.delete("/heros/{hero_id}")
async def delete_hero(hero_id: int, db_session: AsyncSession = Depends(get_db_context)):
    hero = await db_session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    await db_session.delete(hero)
    await db_session.commit()
    return Success()


@router.get("/teams", response_model=list[TeamPublic])
async def read_teams(
    *,
    async_session: AsyncSession = Depends(get_db_context),
    offset: int = 0,
    limit: int = Query(default=2, le=100)
):
    teams = await async_session.execute(select(Team).offset(offset).limit(limit))
    teams = teams.scalars().all()
    return teams


@router.post("/teams", response_model=TeamPublic)
async def create_team(
    *, async_session: AsyncSession = Depends(get_db_context), team: TeamCreate
):
    db_team = Team.model_validate(team)
    async_session.add(db_team)
    await async_session.commit()
    await async_session.refresh(db_team)
    return db_team


@router.get("/teams/{team_id}", response_model=TeamPublic)
async def get_team(team_id: int, async_session: AsyncSession = Depends(get_db_context)):
    db_team = async_session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.patch("/teams/{team_id}", response_model=TeamPublic)
async def update_team(
    team_id: int,
    team: TeamUpdate,
    async_session: AsyncSession = Depends(get_db_context),
):
    db_team = await async_session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    async_session.add(db_team)
    await async_session.commit()
    await async_session.refresh(db_team)
    return db_team


@router.delete("/teams/{team_id}")
async def delete_team(
    team_id: int, async_session: AsyncSession = Depends(get_db_context)
):
    db_team = await async_session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    await async_session.delete(db_team)
    await async_session.commit()
    return Success()
