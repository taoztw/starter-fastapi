import traceback

from fastapi import Request, Depends, HTTPException
from typing import Optional, Dict
from fastapi import Header
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from config import settings
from dependencies import get_db_context
from exts import logger
from exts.exceptions.custom_exc import TokenAuthError
from models import User


async def get_user(
    db_session: AsyncSession = Depends(get_db_context),
    token: Optional[str] = Header(..., description="登录token"),
):
    # validate access jwt token
    error = HTTPException(status_code=401, detail="invalid authorization credentials")
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        if "email" not in payload and "mode" not in payload:
            raise error
        if payload["mode"] != "access_token":
            raise error
        # 检查是否用户存在
        _users = await db_session.execute(
            select(User).where(User.email == payload["email"])
        )
        user = _users.scalars().first()
        if not user:
            raise error
        return user
    except JWTError:
        raise error
    except Exception as e:
        raise error


if __name__ == "__main__":
    payload = jwt.decode(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJpZCI6MSwiZXhwIjoxNzIxNTQ1MTQ1LCJtb2RlIjoiYWNjZXNzX3Rva2VuIn0.KIlMvHasVEUw4lSsYc_DZMbW0ByGcoIZJSxElznIY01",
        settings.SECRET,
        algorithms=[settings.ALGORITHM],
    )
    print(payload)
