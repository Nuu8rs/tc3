import logging

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from database.models.constans import RolePermissionsEnum
from database.models.users import User

class UserRepository:
    @staticmethod
    async def add(
        tx: AsyncSession, 
        user_data: dict
    ) -> User | None:
        user = User(
            name=user_data.get("first_name"),
            login=user_data.get("username", None),
            telegram_id=user_data.get("id"),
            scopes=RolePermissionsEnum.USER
        )
        try:
            tx.add(user)
            await tx.flush()
            await tx.refresh(user)
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            await tx.rollback()
            return None
        return user

    @staticmethod
    async def get(
        tx: AsyncSession,
        id: Optional[int] = None,
        telegram_id: Optional[int] = None,
        login: Optional[int] = None
    ) -> User | None:
        q = select(User)
        if id:
            q = q.where(User.id==id)
        elif telegram_id:
            q = q.where(User.telegram_id==telegram_id)
        elif login:
            q = q.where(User.login==login)
        else:
            return None
        raw = await tx.execute(q)
        return raw.scalar_one_or_none()
