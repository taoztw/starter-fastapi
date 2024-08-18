from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, TIMESTAMP, String

TABLE_PREFIX = "wild_oasis_"


class BookingsBase(SQLModel):
    startDate: datetime | None = Field(
        sa_column=Column(TIMESTAMP(timezone=False), nullable=True)
    )
    endDate: datetime | None = Field(
        sa_column=Column(TIMESTAMP(timezone=False), nullable=True)
    )
    numNights: int | None = Field(default=None)
    numGuests: int | None = Field(default=None)
    cabinPrice: float | None = Field(default=None)
    extrasPrice: float | None = Field(default=None)
    totalPrice: float | None = Field(default=None)
    status: str | None = Field(default=None)
    hasBreakfast: bool | None = Field(default=None)
    isPaid: bool | None = Field(default=None)
    description: str | None = Field(default=None, sa_column=Column(String(500)))


class Bookings(BookingsBase, table=True):
    __tablename__ = f"{TABLE_PREFIX}bookings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    cabinId: str | None = Field(default=None, foreign_key=f"{TABLE_PREFIX}cabins.id")
    guestId: str | None = Field(default=None, foreign_key=f"{TABLE_PREFIX}guests.id")

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    # updated_at: datetime | None = Field(
    #     default_factory=lambda: datetime.now(timezone.utc),
    #     nullable=False,
    #     sa_column_kwargs={
    #         "onupdate": lambda: datetime.now(timezone.utc),
    #     },
    # )
