from sqlalchemy import select

from accounts.session import get_session
from database.models.users import User

from accounts.logger.logger import logger


class UserService:
    
    @classmethod
    async def get_user(cls, id_user: int) -> User| None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = select(User).where(User.id == id_user)
                    result = await sess.execute(stmt)
                    return result.scalar_one_or_none()                    
                except Exception as E:
                    error_message = f"Error fetching user with id_user: {id_user}"
                    logger.error(f"{error_message}\nException: {E}")
        return None