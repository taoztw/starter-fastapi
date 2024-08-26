from sqlmodel import SQLModel, Field
import uuid


class FileBase(SQLModel):
    filepath: str


class File(FileBase, table=True):
    __tablename__ = "files"

    id: str | None = Field(None, primary_key=True)
