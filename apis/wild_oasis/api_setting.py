from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.database_sqlite import async_session
from dependencies import get_db_context
from exts.responses.json_response import Success
from models.wild_oasis.settings import (
    Settings,
    SettingsCreate,
    SettingsRead,
    SettingsUpdate,
)

router = APIRouter()


@router.post("/settings", response_model=SettingsRead)
async def create_settings(
    settings: SettingsCreate, db_session: AsyncSession = Depends(get_db_context)
):
    db_settings = Settings.model_validate(settings)
    db_session.add(db_settings)
    await db_session.commit()
    await db_session.refresh(db_settings)
    return db_settings


@router.get("/settings/{settings_id}", response_model=SettingsRead)
async def read_settings(
    settings_id: str, db_session: AsyncSession = Depends(get_db_context)
):
    settings = await db_session.get(Settings, settings_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings


@router.get("/settings", response_model=list[SettingsRead])
async def read_settings_list(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    db_session: AsyncSession = Depends(get_db_context),
):
    settings_list = await db_session.execute(
        select(Settings).offset(offset).limit(limit)
    )
    settings_list = settings_list.scalars().all()
    return settings_list


@router.patch("/settings/{settings_id}", response_model=SettingsRead)
async def update_settings(
    settings_id: str,
    settings: SettingsUpdate,
    db_session: AsyncSession = Depends(get_db_context),
):
    db_settings = await db_session.get(Settings, settings_id)
    if not db_settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    settings_data = settings.model_dump(exclude_unset=True)
    db_settings.sqlmodel_update(settings_data)
    db_session.add(db_settings)
    await db_session.commit()
    await db_session.refresh(db_settings)
    return db_settings


@router.delete("/settings/{settings_id}")
async def delete_settings(
    settings_id: str, db_session: AsyncSession = Depends(get_db_context)
):
    settings = await db_session.get(Settings, settings_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    await db_session.delete(settings)
    await db_session.commit()
    return Success()
