import asyncio
import time
import os

from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.types import Message, PhotoSize , Document

from accounts.accounts.service.media_downloader import MediaDownloader
from accounts.accounts.service.post_sender import PostSender
from accounts.accounts.service.post_monitoring import PostMonitoring
from accounts.accounts.types import StatusDowloadMedia

from database.models.constans import MediaTypeEnum
from database.models.account_info import AccountInfo
from database.models.posts import Media
from database.models.posts import Post

from accounts.accounts.utils.delete_cta_link import delete_cta_link
from accounts.accounts.utils.time_cache import TimedCache
from accounts.accounts.utils.get_url_patch_media import url_patch_media

from accounts.services.post_service import PostService
from accounts.services.media_service import MediaService

from accounts.logger.logger import logger

from typing import Optional, Any

class NewMessageHandler:
    def __init__(
        self, 
        client: TelegramClient, 
        account_info: AccountInfo, 
        chat_manager
                ) -> None:
        
        
        self.client = client
        self.account_info = account_info
        self.chat_manager = chat_manager
        self.cashed_group = TimedCache()

        self.lock = asyncio.Lock() 

    def _clean_expired_group_ids(self) -> None:
        current_time = int(time.time())
        self.cashed_group = {
            group_id: timestamp 
            for group_id, timestamp in self.cashed_group.items() 
            if timestamp > current_time
        }

    async def handle(self, event: NewMessage.Event) -> None:
        message:Message = event.message
        not_save_media: Media | list[Media] | None = None
        new_post: Optional[Post] = None       
        chat_id = self.chat_manager.get_chat_id(message)
        
        if not chat_id or not self.chat_manager.is_chat_allowed(chat_id):
            return
        
        await asyncio.sleep(0.1)
        
        group_id: int | None = MediaDownloader.get_grouped_id(message)

        async with self.lock:
            if message.media:
                if MediaDownloader.check_status_media_download(message) == StatusDowloadMedia.DOWNLOADING:
                    return MediaDownloader.add_media_to_download(message)
            
            if group_id and not self.cashed_group.get(group_id):
                self.cashed_group.set(group_id, ttl=3)  

            new_post = await PostService.add_new_post(
                message_id    = message.id,
                chat_id       = chat_id,
                text          = delete_cta_link(message.text)
            )
        if new_post:
            media_downloader = MediaDownloader(
                client       = self.client,
                account_info = self.account_info,
                message      = message,
                chat_id      = chat_id,
                post         = new_post
            )
            not_save_media = await media_downloader.download_media()

            post_sender = PostSender(
                post  = new_post,
                media = not_save_media
            )        
            post_monitoring = PostMonitoring(
                client       = self.client,
                account_info = self.account_info,
                post         = new_post
            )
        
            asyncio.create_task(post_monitoring.check_message())
            await post_sender.send_post_to_project()

            if message.media:
                thumbnail_setter = SetThumbnailUrl(
                    post = new_post,
                    not_save_media = not_save_media,
                    message = message,
                    client  = self.client
                )
                await thumbnail_setter.set_thumbnail_url()



class SetThumbnailUrl:
    base_thumbnail_url = "/static/img/no-photo.png"

    def __init__(self,
                 post: Post,
                 not_save_media: list[Media] | Media,
                 message: Message,
                 client: TelegramClient
                 ) -> None:
        
        self.not_save_media = not_save_media
        self.post    = post
        self.message = message
        self.client  = client

        if isinstance(self.not_save_media, Media):
            self.not_save_media = [self.not_save_media]
            
        
    @property
    def first_photo(self) -> Media | None:
        for media in self.not_save_media:
            if media.file_type == MediaTypeEnum.PHOTO:
                return media
        else:
            return None
 
    @property
    def video(self) -> Document | None:
        if hasattr(self.message.media, "video"):
            return self.message.media.document
        return None   
    
    def _get_normal_thumb_photo(self, photos: list[PhotoSize, Any]) -> PhotoSize:
        for photo in photos:
            if type(photo) == PhotoSize:
                return photo
        else:
            return photo[-1]
        
        
    async def get_thumbnail_url_from_video(self, video: Document) -> Media:
        thumbnail_url: str = self.base_thumbnail_url
        try:
            size_photo_preview = self._get_normal_thumb_photo(video.thumbs)
            path_thumb_photo = os.path.join(MediaDownloader.get_static_media_path(), f"photo_thumb_{self.message.id}_{self.post.chat_id}.jpg")
            await self.client.download_media(
                message = self.message,
                file = path_thumb_photo,
                thumb = size_photo_preview
            )
            thumbnail_url = path_thumb_photo.replace("accounts","").replace("\\","/")
        except Exception as E:
            logger.error(f"Error {E} get thumbnail url from video")
        finally:
            return thumbnail_url
        
    async def set_thumbnail_url(self):
        thumbnail_url: str = self.base_thumbnail_url
        
        if self.first_photo:
            thumbnail_url = self.first_photo.file_url
        
        if self.video:
            thumbnail_url = await self.get_thumbnail_url_from_video(
                video = self.video)

                
        return await self._save_new_thumbnail_url(
            thumbnail_url
        )    
    
    async def _save_new_thumbnail_url(self, thumbnail_url: str) -> None:
        await PostService.set_thumbnail_url(
            post_id = self.post.id,
            thumbnail_url = thumbnail_url
        )
        await self._save_media()
        
    async def _save_media(self) -> None:
        for media in self.not_save_media:
            await MediaService.add_new_media(
                post_id   = self.post.id,
                file_url  = media.file_url,
                file_type = media.file_type  
            )