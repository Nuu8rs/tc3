from sqlalchemy import insert, select

from accounts.session import get_session
from database.models.chats import Chat

from accounts.logger.logger import logger

class ChatTelegramService:

    @classmethod
    async def add_new_chat(cls, chat_link: str, chat_id: int, 
                           chat_name: str, chat_type: str) -> Chat | None:
        async for session in get_session():
            async with session as sess:  
                try:
                    new_chat = Chat(
                        chat_id    = chat_id,
                        chat_link  = chat_link,
                        chat_name  = chat_name,
                        chat_type  = chat_type,
                    )

                    sess.add(new_chat)
                    await sess.commit()
                    return new_chat
                except Exception as E:
                    error_message = f"Error adding new chat {chat_name} with chat_id: {chat_id}"
                    logger.error(f"{error_message}\nException: {E}")
        return None

    @classmethod
    async def get_chat(cls, chat_id: int) -> Chat | None:
        async for session in get_session():
            async with session as sess:  
                try:
                    stmt = (
                        select(Chat)
                        .where(Chat.chat_id == chat_id)
                    )
                    result = await session.execute(stmt)
                    return result.scalar_one_or_none()
                except Exception as E:
                    error_message = f"Error get chat chat_od : {chat_id}"
                    logger.error(f"{error_message}\nException: {E}")
        return None