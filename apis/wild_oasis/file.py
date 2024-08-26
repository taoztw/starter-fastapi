import os.path
import uuid
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from dependencies import get_db_context
from models.file import File
import aiofiles

router = APIRouter()


@router.post("/upload", response_model=File)
async def upload_file(
    file: UploadFile, db_session: AsyncSession = Depends(get_db_context)
):
    file_id = uuid.uuid4().hex
    filename = f"{file_id}_{file.filename}"
    file_save_path = os.path.join(settings.CABIN_STATIC_DIR, filename)

    async with aiofiles.open(file_save_path, "wb") as f:
        while content := await file.read(1024):  # 一次读取1024字节
            await f.write(content)

    db_file = File(id=file_id, filepath=f"static/cabin_static/{filename}")
    db_session.add(db_file)
    await db_session.commit()
    await db_session.refresh(db_file)
    return db_file
