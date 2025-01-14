import re
import traceback

from database.models.users import User
from bot.session import get_session
from sqlalchemy import select

from bot.logger.logger import logger


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
    
    
    @classmethod
    async def get_user_by_user_id(cls, user_id: int) -> User|None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = select(User).where(User.telegram_id == user_id)
                    result = await sess.execute(stmt)
                    return result.scalar_one_or_none()                    
                except Exception as E:
                    error_message = f"Error fetching user with user_id: {user_id}"
                    logger.error(f"{error_message}\nException: {E}")
        return None
        
    
    @classmethod
    async def create_user(cls, full_name: str, user_name: str, user_id: int, language: str) -> User:
        async for session in get_session():
            async with session as sess: 
                try:
                    user = User(
                        name        = full_name,
                        login       = user_name,
                        telegram_id = user_id,
                        language    = language
                    )
                    sess.add(user)
                    await sess.commit()
                    return user
                except Exception as E:
                    error_message = f"Error create user with user_id: {user_id}| full_name: {full_name}| user_name: {user_name}"
                    logger.error(f"{error_message}\nException: {E}")