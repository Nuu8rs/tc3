from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from database.models.users import User
from database.models.auth import Auth


class AuthRepository:
    @staticmethod
    async def add(
        tx: AsyncSession, 
        user: User, 
        token: str
    ) -> Auth | None:
        try:
            auth = Auth(token=token, user_id=user.id)
            tx.add(auth)
            await tx.flush()
            await tx.refresh(auth)
        except IntegrityError:
            await tx.rollback()
            return None
        return auth

    @staticmethod
    async def get(
        tx: AsyncSession,
        token: str
    ) -> Auth | None:
        q = select(Auth).where(
            Auth.token == token
        )
        raw = await tx.execute(q)
        return raw.scalar_one_or_none()
