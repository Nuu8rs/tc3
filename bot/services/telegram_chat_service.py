from database.models.chats import Chat
from bot.session import get_session
from sqlalchemy import insert

from bot.logger.logger import logger

class ChatTelegramService:

    @classmethod
    async def add_new_chat(cls, chat_link: str, chat_id: int, 
                           chat_name: str, chat_type: str, 
                           project_id: int) -> Chat | None:
        async for session in get_session():
            async with session as sess:  
                try:
                    new_chat = Chat(
                        chat_id    = chat_id,
                        chat_link  = chat_link,
                        chat_name  = chat_name,
                        chat_type  = chat_type,
                        project_id = project_id
                    )

                    sess.add(new_chat)
                    await sess.commit()
                    return new_chat
                except Exception as E:
                    error_message = f"Error adding new chat {chat_name} with chat_id: {chat_id}"
                    logger.error(f"{error_message}\nException: {E}")
        return None
