import asyncio

from telethon import TelegramClient
from accounts.accounts.manager.join_chat_manager import JoinChatManager

from database.models.account_info import AccountInfo
from database.models.chats import Chat

from accounts.services.telegram_chat_service import ChatTelegramService
from accounts.services.chat_association_service import ChatAssociationService
from accounts.services.project_chat_association_service import ProjceChatAssociationService

from .manager.chat_account_manager import ChatAccountManager
from .types import ResultJoinToChat, ResultJoin

from accounts.logger.logger import logger

class Account:
    
    def __init__(self, client:TelegramClient, account_info: AccountInfo):
        self.client = client
        self.account_info = account_info
        self.join_chat_manager = JoinChatManager(client,account_info)
        self.chat_account_manager = ChatAccountManager(client,account_info)
             
        
    async def start_listening(self):
        await self.chat_account_manager.iniatilization_chats()
        
        await self.client.run_until_disconnected()
        
        
    async def disconnect(self):
        await self.client.disconnect()
        logger.info(f"Аккаунт {self.account_info.session_name} отключён.")
        
    async def join_to_chat(self, chat_link: str, project_id: int) -> ResultJoinToChat:
        chat_join_result:ResultJoinToChat =  await self.join_chat_manager.join_to_chat(chat_link, project_id)
        
        if chat_join_result.join_status in [ResultJoin.SUCCES_JOIN, ResultJoin.ALREADY_JOIN]:
            await asyncio.sleep(0.01)
            tg_chat = None
            
            tg_chat: Chat | None = await ChatTelegramService.get_chat(
                chat_id = chat_join_result.chat_id
            )
            if not tg_chat:
                tg_chat = await ChatTelegramService.add_new_chat(
                    chat_link  = chat_link,
                    chat_id    = chat_join_result.chat_id,
                    chat_name  = chat_join_result.chat_title,
                    chat_type  = chat_join_result.type_chat,
                )
            
            await ChatAssociationService.add_new_association(
                account_id=self.account_info.id,
                chat_id=tg_chat.chat_id
            )

            await ProjceChatAssociationService.add_new_project_chat_association(
                chat_id    = chat_join_result.chat_id,
                project_id = project_id
            )

            self.chat_account_manager.add_to_views_chat(
                chat_id=chat_join_result.chat_id
            )
        return chat_join_result