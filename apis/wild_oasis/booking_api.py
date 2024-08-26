# routes/bookings.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from dependencies import get_db_context
from models.wild_oasis.bookings import (
    Bookings,
    BookingsCreate,
    BookingsRead,
    BookingsUpdate,
)

router = APIRouter()


# 创建 Booking
@router.post("/bookings", response_model=BookingsRead)
async def create_booking(
    booking: BookingsCreate, db_session: AsyncSession = Depends(get_db_context)
):
    db_booking = Bookings.from_orm(booking)
    db_session.add(db_booking)
    await db_session.commit()
    await db_session.refresh(db_booking)
    return db_booking


# 获取所有 Bookings
@router.get("/bookings", response_model=list[BookingsRead])
async def read_bookings(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    db_session: AsyncSession = Depends(get_db_context),
):
    bookings = await db_session.execute(select(Bookings).offset(offset).limit(limit))
    bookings = bookings.scalars().all()
    return bookings


# 根据ID获取特定 Booking
@router.get("/bookings/{booking_id}", response_model=BookingsRead)
async def read_booking(
    booking_id: str, db_session: AsyncSession = Depends(get_db_context)
):
    booking = await db_session.get(Bookings, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# 更新 Booking
@router.patch("/bookings/{booking_id}", response_model=BookingsRead)
async def update_booking(
    booking_id: str,
    booking: BookingsUpdate,
    db_session: AsyncSession = Depends(get_db_context),
):
    db_booking = await db_session.get(Bookings, booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    update_data = booking.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_booking, key, value)

    db_session.add(db_booking)
    await db_session.commit()
    await db_session.refresh(db_booking)
    return db_booking


# 删除 Booking
@router.delete("/bookings/{booking_id}")
async def delete_booking(
    booking_id: str, db_session: AsyncSession = Depends(get_db_context)
):
    booking = await db_session.get(Bookings, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    await db_session.delete(booking)
    await db_session.commit()
    return {"message": "Booking deleted successfully"}
