import asyncio

from telethon.events import MessageEdited
from telethon.tl.types import Message

from database.models.constans import PostStatusEnum
from database.models.posts import Post

from accounts.services.post_service import PostService

#TODO КОГДА ПОСТ ОБНОВИЛИ ДЕЛАЕМ НОВЫЙ ПОСТ ИЛИ ИЗМЕНЯЕМ СТАРЫЙ?


class MessageEditHandler:
    def __init__(self, client, account_info, chat_manager) -> None:
        self.client = client
        self.account_info = account_info
        self.chat_manager = chat_manager
        
    async def handle(self, event: MessageEdited.Event) -> None:
        message: Message = event.message
        
        if not hasattr(event, "chat_id"):
            return

        chat_id = self.chat_manager.get_chat_id(message)
        if not chat_id or not self.chat_manager.is_chat_allowed(chat_id):
            return
        
        await asyncio.sleep(0.1)
        await PostService.edit_was_change(
            message_id      = message.id,
            chat_id         = chat_id,
            new_status_post = PostStatusEnum.EDITED
        )
        