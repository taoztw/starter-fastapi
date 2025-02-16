from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from dependencies import get_db_context
from exts.responses.json_response import Success
from models.wild_oasis.cabins import (
    Cabins,
    CabinsCreate,
    CabinsRead,
    CabinsUpdate,
)

router = APIRouter()


# 创建 Cabin
@router.post("/cabins", response_model=CabinsRead)
async def create_cabin(
    cabin: CabinsCreate, db_session: AsyncSession = Depends(get_db_context)
):
    db_cabin = Cabins.from_orm(cabin)
    db_session.add(db_cabin)
    await db_session.commit()
    await db_session.refresh(db_cabin)
    return db_cabin


# 获取所有 Cabins
@router.get("/cabins", response_model=list[CabinsRead])
async def read_cabins(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    db_session: AsyncSession = Depends(get_db_context),
):
    cabins = await db_session.execute(select(Cabins).offset(offset).limit(limit))
    cabins = cabins.scalars().all()
    return cabins


# 根据ID获取特定 Cabin
@router.get("/cabins/{cabin_id}", response_model=CabinsRead)
async def read_cabin(cabin_id: str, db_session: AsyncSession = Depends(get_db_context)):
    cabin = await db_session.get(Cabins, cabin_id)
    if not cabin:
        raise HTTPException(status_code=404, detail="Cabin not found")
    return cabin


# 更新 Cabin
@router.patch("/cabins/{cabin_id}", response_model=CabinsRead)
async def update_cabin(
    cabin_id: str,
    cabin: CabinsUpdate,
    db_session: AsyncSession = Depends(get_db_context),
):
    db_cabin = await db_session.get(Cabins, cabin_id)
    if not db_cabin:
        raise HTTPException(status_code=404, detail="Cabin not found")

    update_data = cabin.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cabin, key, value)

    db_session.add(db_cabin)
    await db_session.commit()
    await db_session.refresh(db_cabin)
    return db_cabin


# 删除 Cabin
@router.delete("/cabins/{cabin_id}")
async def delete_cabin(
    cabin_id: str, db_session: AsyncSession = Depends(get_db_context)
):
    cabin = await db_session.get(Cabins, cabin_id)
    if not cabin:
        raise HTTPException(status_code=404, detail="Cabin not found")

    await db_session.delete(cabin)
    await db_session.commit()
    return {"message": "Cabin deleted successfully"}
