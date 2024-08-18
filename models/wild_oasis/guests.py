from datetime import datetime

from sqlalchemy import Column, TIMESTAMP
from sqlmodel import SQLModel, Field
import uuid

TABLE_PREFIX = "wild_oasis_"


class GuestsBase(SQLModel):

    fullName: str | None = Field(default=None)
    email: str | None = Field(default=None)
    nationalID: str | None = Field(default=None)
    nationality: str | None = Field(default=None)
    countryFlag: str | None = Field(default=None)


class Guests(GuestsBase, table=True):
    __tablename__ = f"{TABLE_PREFIX}guests"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
