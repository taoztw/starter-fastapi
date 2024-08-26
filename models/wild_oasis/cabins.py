from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, String
from sqlmodel import SQLModel, Field
import uuid

TABLE_PREFIX = "wild_oasis_"


class CabinsBase(SQLModel):

    name: str | None = Field(default=None)
    maxCapacity: int | None = Field(default=None)
    regularPrice: float | None = Field(default=None)
    discount: int | None = Field(default=None)
    description: str | None = Field(
        default=None, sa_column=Column(String(500))
    )  # 设置字符限制
    image: str | None = Field(default=None)


class Cabins(CabinsBase, table=True):
    __tablename__ = f"{TABLE_PREFIX}cabins"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class CabinsCreate(CabinsBase):
    pass


class CabinsRead(CabinsBase):
    id: str
    created_at: datetime


class CabinsUpdate(CabinsBase):
    name: str | None = None
    maxCapacity: int | None = None
    regularPrice: float | None = None
    discount: int | None = None
    description: str | None = None
    image: str | None = None
