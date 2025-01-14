import asyncio

from telethon import TelegramClient
from telethon.events import MessageDeleted 
from database.models.constans import PostStatusEnum

from database.models.account_info import AccountInfo

from accounts.services.post_service import PostService

class MessageDeleteHandler:
    def __init__(
            self, 
            client: TelegramClient, 
            account_info: AccountInfo, 
            chat_manager
            ) -> None:
        
        self.client = client
        self.account_info = account_info
        self.chat_manager = chat_manager

    async def handle(self, event: MessageDeleted.Event) -> None:
        message_ids:list[int] = event.deleted_ids
        if not getattr(event, "chat_id", None):
            return
        
        chat_id = int(str(event.chat_id).replace("-100",""))
        
        if not chat_id or not self.chat_manager.is_chat_allowed(chat_id):
            return
        
        await asyncio.sleep(0.1)
        for message_id in message_ids:
            await PostService.edit_was_change(
                message_id      = message_id,
                chat_id         = chat_id,
                new_status_post = PostStatusEnum.DELETED
            )
        