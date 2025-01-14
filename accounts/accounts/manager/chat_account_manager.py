import asyncio

from accounts.accounts.manager.chat_event_manager import ChatEvents

from telethon import TelegramClient
from telethon.tl.types import Message

from database.models.account_chat_association import AccountChatAssociation
from database.models.account_info import AccountInfo
from database.models.chats import Chat

from accounts.services.chat_association_service import ChatAssociationService
from accounts.services.chat_service import ChatService

from typing import Sequence

from accounts.logger.logger import logger



class ChatAccountManager:
    
    def __init__(self, client: TelegramClient, account_info: AccountInfo) -> None:
        self.client = client
        self.account_info = account_info
        self.chat_event_manager = ChatEvents(client, account_info, self)
        self.chats_views: set = set()
        
    async def iniatilization_chats(self) -> None:
        logger.info(self.account_info.prefix_log + "Начинаю добавлять чаты к аккаунту")
        all_chat_asscociation_by_account: Sequence[AccountChatAssociation] = (
            await ChatAssociationService.get_id_chats_by_account_id(
                account_id=self.account_info.id
            )
        )
        if not all_chat_asscociation_by_account:
            return self.chat_event_manager.register_handlers()
        
        chats_ids: list[int]   = [chat_association.chat_id for chat_association in all_chat_asscociation_by_account]
        all_chats: list[Chat] = await ChatService.get_chats(chats_ids)
        
        for chat in all_chats:
            self.add_to_views_chat(chat_id=chat.chat_id)    
        
        return self.chat_event_manager.register_handlers()

        
    def add_to_views_chat(self, chat_id: int) -> None:
        self.chats_views.add(chat_id)
        
    def is_chat_allowed(self, chat_id: int) -> bool:
        return chat_id in self.chats_views
    
    @staticmethod
    def get_chat_id(message: Message) -> int | None:
        if getattr(message.peer_id, "user_id", None):
            return None 
        return message.peer_id.channel_id if hasattr(message.peer_id, "channel_id") else message.peer_id.chat_id
        