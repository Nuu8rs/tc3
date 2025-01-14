import asyncio

from telethon import TelegramClient
from telethon.events import Raw
from telethon.tl.types import Message, MessageMediaPhoto, MessageMediaDocument

from accounts.accounts.service.media_downloader import MediaDownloader
from accounts.accounts.service.post_sender import PostSender
from accounts.accounts.service.post_monitoring import PostMonitoring
from accounts.accounts.types import StatusDowloadMedia

from database.models.account_info import AccountInfo
from database.models.posts import Media
from database.models.posts import Post

from accounts.accounts.utils.delete_cta_link import delete_cta_link

from accounts.services.post_service import PostService

from typing import Optional

class RawHandler:
    def __init__(self, client, account_info, chat_manager) -> None:
        self.client = client
        self.account_info = account_info
        self.chat_manager = chat_manager
        
    async def handle(self, event: Raw):
        print(event)