import os
from aiogram import Bot

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from database.models.posts import Media
from database.models.posts import Post
from database.models.projects import Project
from database.models.constans import MediaTypeEnum

from functools import wraps

from bot.config import config
from bot.logger.logger import logger


def log_exceptions(method):
    @wraps(method)
    async def wrapper(*args, **kwargs):
        try:
            return await method(*args, **kwargs)
        except Exception as e:
            self = args[0]
            logger.error(f"Error in {method.__name__} | post_id: {self.post.id} | error: {e}")
    return wrapper

class SenderPostsToProject:
    bot = Bot(token=config.bot_config.BOT_TOKEN, 
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    def __init__(self, post: Post, project: Project, media: list[Media] | Media = None) -> None:
        self.post = post
        self.project = project 
        self.media = media
        
    @staticmethod
    def patch_path(path: str):
        if path.startswith("/"):
            path = path[1:]
        return os.path.join("accounts",path)    

    
    async def send_message(self):
        if not self.media:
            return await self._send_post_message()
        
        if isinstance(self.media, list):
            return await self._send_post_media_group() 
        
        if self.media.file_type == MediaTypeEnum.PHOTO:
            return await self._send_post_photo()
        
        if self.media.file_type == MediaTypeEnum.VIDEO:
            return await self._send_post_video()

    @log_exceptions      
    async def _send_post_media_group(self): 
        media_group = MediaGroupBuilder(caption = self.post.text)
        for current_media in self.media:
            media_group.add(
                type  = current_media.file_type.value.lower(),
                media = FSInputFile(
                    path     = self.patch_path(current_media.file_url),
                    filename = current_media.file_url.split("/")[-1]        
                                    )
            )
            
        await self.bot.send_media_group(
            chat_id = self.project.chat_id,
            media   = media_group.build()
                                    )

    
    @log_exceptions
    async def _send_post_video(self):
        video = FSInputFile(
            path     = self.patch_path(self.media.file_url), 
            filename = self.media.file_url.split("/")[-1]
                        )
        
        await self.bot.send_video(
            chat_id      = self.project.chat_id,
            video        = video,
            caption      = self.post.text,
                            )

            
    @log_exceptions
    async def _send_post_photo(self):
        logger.info(self.patch_path(self.media.file_url))
        photo = FSInputFile(
            path     = self.patch_path(self.media.file_url), 
            filename = self.media.file_url.split("/")[-1]
                        )
        
        await self.bot.send_photo(
            chat_id      = self.project.chat_id,
            photo        = photo,
            caption      = self.post.text
                            )   

    @log_exceptions
    async def _send_post_message(self):
        await self.bot.send_message(
            chat_id = self.project.chat_id,
            text    = self.post.text
                              )
