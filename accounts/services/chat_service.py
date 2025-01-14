from sqlalchemy import select

from accounts.session import get_session
from accounts.logger.logger import logger
from database.models.chats import Chat



class ChatService:
    
    @classmethod
    async def get_chats(self, chats_ids: list[int]) -> list[Chat]:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = select(Chat).where(Chat.chat_id.in_(chats_ids))
                    result = await sess.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    error_message = f"Error while fetching chats with IDs {chats_ids}: {str(E)}"
                    logger.error(f"{error_message}")
                    
    @classmethod
    async def get_chat(self, chat_id: int) -> Chat | None:
        async for session in get_session():
            async with session as sess: 
                try:
                    stmt = select(Chat).where(Chat.chat_id == chat_id)
                    result = await sess.execute(stmt)
                    return result.scalar_one_or_none()
                except Exception as E:
                    error_message = f"Error while fetching chat with ID {chat_id}: {str(E)}"
                    logger.error(f"{error_message}")