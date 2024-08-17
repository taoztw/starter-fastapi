from typing import Optional

from fastapi import HTTPException, status, Header
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from config import settings
from datetime import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from exts import logger

from dependencies import get_db_context
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
error = HTTPException(status_code=401, detail="invalid authorization credentials")


def create_access_token(data):
    data["exp"] = datetime.utcnow() + settings.JWT_ACCESS_EXP
    data["mode"] = "access_token"
    return jwt.encode(data, settings.SECRET, algorithm=settings.ALGORITHM)


def create_refresh_token(data):
    data["exp"] = datetime.utcnow() + settings.JWT_REFRESH_EXP
    data["mode"] = "refresh_token"
    return jwt.encode(data, settings.SECRET, algorithm=settings.ALGORITHM)


async def authorize(
    token: Optional[str] = Header(..., description="登录token"),
    db_session: AsyncSession = Depends(get_db_context),
) -> dict:
    # validate refresh jwt token
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])

        if "email" not in payload and "mode" not in payload:
            raise error
        if payload["mode"] != "refresh_token":
            raise error
        # 检查是否用户存在
        result = await db_session.execute(
            select(User).where(User.email == payload["email"])
        )
        user = result.scalars().first()
        if not user or token != user.refresh_token:
            raise error

        # 生成新的refresh token并且更新用户
        data = {"email": user.email, "id": user.id}
        refresh_token = create_refresh_token(data)
        user.sqlmodel_update({"refresh_token": refresh_token})
        db_session.add(user)
        await db_session.commit()
        access_tkn = create_access_token(data)
        return {
            "access_token": access_tkn,
            "refresh_token": refresh_token,
            "email": user.email,
            "type": "bearer",
        }
    except JWTError:
        raise error
