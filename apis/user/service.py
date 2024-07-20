from typing import List, Optional

from sqlalchemy import select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


class UserServices:
    @staticmethod
    async def is_user_exist(async_session: AsyncSession, user_id: int) -> bool:
        result = await async_session.execute(
            select(User).where(User.id == user_id, User.is_delete == False)
        )
        return result.scalar() is not None

    @staticmethod
    async def reset_password(
        async_session: AsyncSession, email: str, password_hash: str
    ) -> Optional[User]:
        await async_session.execute(
            update(User)
            .where(User.email == email, User.is_delete == False)
            .values(password_hash=password_hash)
        )
        await async_session.commit()

    @staticmethod
    async def update_refresh_token(
        async_session: AsyncSession, email: str, refresh_token: str
    ) -> Optional[User]:
        # 执行更新操作
        await async_session.execute(
            update(User)
            .where(User.email == email, User.is_delete == False)
            .values(refresh_token=refresh_token)
        )
        # 提交事务
        await async_session.commit()

        # 查询更新后的用户数据
        query = select(User).where(User.email == email, User.is_delete == False)
        result = await async_session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def is_email_exist(async_session: AsyncSession, email: str) -> bool:
        result = await async_session.execute(
            select(User).where(User.email == email, User.is_delete == False)
        )
        return result.scalar() is not None

    @staticmethod
    async def get_user(async_session: AsyncSession, user_id: int) -> Optional[User]:
        result = await async_session.execute(
            select(User).where(User.id == user_id, User.is_delete == False)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(
        async_session: AsyncSession, email: str
    ) -> Optional[User]:
        result = await async_session.execute(
            select(User).where(User.email == email, User.is_delete == False)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_users(async_session: AsyncSession) -> List[User]:
        result = await async_session.execute(
            select(User).where(User.is_delete == False).order_by(User.id.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def create_user(async_session: AsyncSession, **kwargs) -> User:
        new_user = User(**kwargs)
        async_session.add(new_user)
        await async_session.commit()
        return new_user

    @staticmethod
    async def update_user(
        async_session: AsyncSession, user_id: int, **kwargs
    ) -> Optional[User]:
        response = (
            update(User)
            .where(User.id == user_id, User.is_delete == False)
            .values(**kwargs)
            .returning(User)
        )
        result = await async_session.execute(response)
        await async_session.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_user(async_session: AsyncSession, user_id: int) -> None:
        await async_session.execute(
            update(User).where(User.id == user_id).values(is_delete=True)
        )
        await async_session.commit()

    @staticmethod
    async def search_user(async_session: AsyncSession, keywords: str) -> List[User]:
        result = await async_session.execute(
            select(User)
            .where(
                or_(
                    User.email.ilike(f"%{keywords}%"),
                    User.password_hash.ilike(f"%{keywords}%"),
                    User.refresh_token.ilike(f"%{keywords}%"),
                ),
                User.is_delete == False,
            )
            .order_by(User.id.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def batch_delete_user(
        async_session: AsyncSession, user_ids: List[int]
    ) -> None:
        # 检查要删除的用户是否都存在
        existing_users = (
            (
                await async_session.execute(
                    select(User.id).where(
                        User.id.in_(user_ids), User.is_delete == False
                    )
                )
            )
            .scalars()
            .all()
        )

        if len(existing_users) != len(user_ids):
            await async_session.rollback()
            raise ValueError("One or more users do not exist or are already deleted.")

        # 批量逻辑删除用户
        await async_session.execute(
            update(User).where(User.id.in_(user_ids)).values(is_delete=True)
        )
        await async_session.commit()
