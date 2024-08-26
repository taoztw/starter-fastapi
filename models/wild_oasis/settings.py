from datetime import datetime

from sqlalchemy import Column, TIMESTAMP
from sqlmodel import SQLModel, Field
import uuid

TABLE_PREFIX = "wild_oasis_"


class SettingsBase(SQLModel):
    minBookingLength: int | None = Field(default=None)
    maxBookingLength: int | None = Field(default=None)
    maxGuestsPerBooking: int | None = Field(default=None)
    breakfastPrice: float | None = Field(default=None)


class Settings(SettingsBase, table=True):
    __tablename__ = f"{TABLE_PREFIX}settings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class SettingsCreate(SettingsBase):
    pass


class SettingsRead(SettingsBase):
    id: str
    created_at: datetime


class SettingsUpdate(SettingsBase):
    pass
