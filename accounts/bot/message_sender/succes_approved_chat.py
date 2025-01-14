from database.models.projects import Project
from accounts.services.user_service import UserService

from accounts.logger.logger import logger

from accounts.config import bot_teletracker


class SendMessageSuccesApprovedChat:
    bot = bot_teletracker
    def __init__(self, project: Project, chat_name: str) -> None:
        self.project = project 
        self.chat_name = chat_name
    
    
    async def send_succes_join_chat(self):
        try:
            user = await UserService.get_user(
                id_user = self.project.user_id 
                )
            if not user:
                return 
            
            await self.bot.send_message(
                chat_id = user.telegram_id,
                text = "Бота успешно добавили в чат {chat_name}".format(
                    chat_name = self.chat_name
                )
            )
        except Exception as E:
            logger.error(f"Err {E} send message to succes approved user to chat {self.chat_name}")