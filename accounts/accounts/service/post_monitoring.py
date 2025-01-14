import asyncio
from datetime import datetime

from telethon import TelegramClient 
from telethon.tl.types import Message, TypePeer, PeerChat, PeerChannel

from database.models.account_info import AccountInfo 
from database.models.posts import Post
from database.models.posts import Views

from accounts.services.views_service import ViewService

from accounts.constans import TIME_WAIT_CHECK_POST_VIEWS

from accounts.logger.logger import logger

from typing import Optional

class PostMonitoring:
    
    def __init__(self, client: TelegramClient, account_info: AccountInfo, post: Post):
        self.client       = client
        self.account_info = account_info
        self.logger_prefix: str = f"[Аккаунт {account_info.session_name}]"
        self.post = post
        
    async def check_message(self) -> None:
        for time_wait in TIME_WAIT_CHECK_POST_VIEWS:
            views: Optional[Views] = await ViewService.add_new_views(
                chat_id    = self.post.chat_id,
                message_id = self.post.message_id,
            )
            if not views:
                return None
            
            await self._wait_to_check(
                time_to_sleep = time_wait.total_seconds(),
                views         = views
            )    
        
    async def _wait_to_check(self, time_to_sleep: int, views: Views):
        await asyncio.sleep(time_to_sleep)
        await self._check_views_post(views)
    
    async def _check_views_post(self, views: Views):
        try:
            message = await self.client.get_messages(
                self.post.chat_id,
                ids = [self.post.message_id]
            )
            current_message = message[0]
            if not isinstance(current_message, Message):
                if current_message is None:
                    #TODO СДЕЛАТЬ ТО ЧТО СООБЩЕНИЕ УДАЛЕНО
                    pass
                return 
            
            amount_views: int = getattr(current_message, "views", None)
            
            if not amount_views:
                return
            
            await ViewService.update_amount_views(
                id_views     = views.id,
                amount_views = amount_views
            )
        except Exception as E:
            logger.error(E)
    # @classmethod
    # async def 
        
        
        