from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.database_sqlite import async_session
from dependencies import get_db_context
from exts.responses.json_response import Success
from models.wild_oasis.guests import Guests, GuestsCreate, GuestsRead, GuestsUpdate

router = APIRouter()


@router.post("/guests", response_model=GuestsRead)
async def create_guest(
    guest: GuestsCreate, db_session: AsyncSession = Depends(get_db_context)
):
    db_guest = Guests.model_validate(guest)
    db_session.add(db_guest)
    await db_session.commit()
    await db_session.refresh(db_guest)
    return db_guest


@router.get("/guests/{guest_id}", response_model=GuestsRead)
async def read_guest(guest_id: str, db_session: AsyncSession = Depends(get_db_context)):
    guest = await db_session.get(Guests, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest


@router.get("/guests", response_model=list[GuestsRead])
async def read_guests(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    db_session: AsyncSession = Depends(get_db_context),
):
    guests_list = await db_session.execute(select(Guests).offset(offset).limit(limit))
    guests_list = guests_list.scalars().all()
    return guests_list


@router.patch("/guests/{guest_id}", response_model=GuestsRead)
async def update_guest(
    guest_id: str,
    guest: GuestsUpdate,
    db_session: AsyncSession = Depends(get_db_context),
):
    db_guest = await db_session.get(Guests, guest_id)
    if not db_guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    guest_data = guest.model_dump(exclude_unset=True)
    db_guest.sqlmodel_update(guest_data)
    db_session.add(db_guest)
    await db_session.commit()
    await db_session.refresh(db_guest)
    return db_guest


@router.delete("/guests/{guest_id}")
async def delete_guest(
    guest_id: str, db_session: AsyncSession = Depends(get_db_context)
):
    guest = await db_session.get(Guests, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    await db_session.delete(guest)
    await db_session.commit()
    return Success()
