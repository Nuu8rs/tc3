import os
import asyncio
from pathlib import Path

from accounts.accounts.types import StatusDowloadMedia

from database.models.account_info import AccountInfo
from database.models.posts import Media
from database.models.posts import Post
from database.models.constans import MediaTypeEnum

from collections import defaultdict

from telethon import TelegramClient
from telethon.tl.types import Message, TypeMessageMedia, MessageMediaPhoto, MessageMediaDocument, PhotoSize

from accounts.logger.logger import logger

def callback(current, total):
    print('Downloaded', current, 'out of', total,
            'bytes: {:.2%}'.format(current / total))




class MediaDownloader:
    _group_locks:defaultdict = defaultdict(asyncio.Lock)
    _active_downloads: set = set() 
    _media_list:defaultdict = defaultdict(list[TypeMessageMedia])
    
    types_file = {
        MessageMediaPhoto : MediaTypeEnum.PHOTO,
        MessageMediaDocument : MediaTypeEnum.VIDEO,
    }
    
    TIME_TO_CHECK_APPEND_MEDIA_STACK = 3
    
    def __init__(
            self, 
            client: TelegramClient, 
            account_info: AccountInfo, 
            message: Message,
            chat_id: int,
            post: Post
                ) -> None:
        
        self.client = client
        self.account_info = account_info
        self.message = message
        self.chat_id = chat_id
        self.post = post
        
        self.logger_prefix = f"[Аккаунт {account_info.session_name}] "
    
    @staticmethod
    def get_grouped_id(message: Message) -> int | None:
        return getattr(message, "grouped_id", None)
    
    @classmethod
    def check_status_media_download(cls, message: Message) -> StatusDowloadMedia:
        grouped_id = cls.get_grouped_id(message)
        
        if grouped_id in cls._active_downloads:
            return StatusDowloadMedia.DOWNLOADING
        
        return StatusDowloadMedia.NOT_DOWNLOADING

    @classmethod
    def add_media_to_download(cls, message: Message) -> None:
        grouped_id = cls.get_grouped_id(message)
        cls._media_list[grouped_id].append(message.media)
        
    async def download_media(self) -> list[Media] | Media | None:
        grouped_id: int | None = self.get_grouped_id(self.message)
        
        if not grouped_id:
            return await self.download_media_(self.message.media)

        self._active_downloads.add(grouped_id)
        self.add_media_to_download(message=self.message)
        
        try:
            return await self._download_media_group(grouped_id)
        except Exception as E:
            logger.error(f"{self.logger_prefix} Ошибка при загрузке группы {grouped_id}: {E}")
    
        finally:
            self._active_downloads.remove(grouped_id)
            self._media_list.pop(grouped_id, None)
            
        return None
                                
    async def _download_media_group(self, group_id: int) -> list[Media]:
        await asyncio.sleep(self.TIME_TO_CHECK_APPEND_MEDIA_STACK)
        media_group = []
        for media in self._media_list[group_id]:
            media:Media = await self.download_media_(media)
            media_group.append(media)
            
        return media_group
    
    @staticmethod
    def get_static_media_path():
        static_media_path = os.path.join('accounts','static', 'media')
        
        os.makedirs(static_media_path, exist_ok=True)
        
        return static_media_path

    
    
    async def download_media_(self, media: TypeMessageMedia) -> Media | None:
        
        if not isinstance(media, (MessageMediaPhoto, MessageMediaDocument)):
            return None
        
        file_patch = await self.client.download_media(
            media, 
            file= self.get_static_media_path(),
            )
        
        file_type = MediaDownloader.types_file.get(type(media))
        file_patch = file_patch.replace("accounts","").replace("\\","/")
        return Media(
            post_id   = self.post.id,
            file_url  = file_patch,
            file_type = file_type
        )
