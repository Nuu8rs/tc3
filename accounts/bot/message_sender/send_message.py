import os

from aiogram.types import InlineKeyboardMarkup, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from accounts.bot.keyboards.keyboard_post import select_options_for_post
from functools import wraps

from database.models.posts import Media
from database.models.posts import Post
from database.models.projects import Project
from database.models.users import User
from database.models.constans import MediaTypeEnum

from accounts.services.user_service import UserService

from accounts.logger.logger import logger

from accounts.config import bot_teletracker

def log_exceptions(method):
    @wraps(method)
    async def wrapper(*args, **kwargs):
        try:
            return await method(*args, **kwargs)
        except Exception as e:
            self = args[0]
            logger.error(f"Error in {method.__name__} | post_id: {self.post.id} | error: {e}")
    return wrapper


class SendMessager:
    bot = bot_teletracker
    
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
        user: User = await UserService.get_user(id_user = self.project.user_id)
    
        if not user:
            logger.error(f"Не смог найти пользователя, id_user: {self.project.user_id}")
            return
        
        keyboard = select_options_for_post(
            post_id    = self.post.id,
            project_id = self.project.id
        )
        
        if not self.media:
            return await self._send_post_message(chat_id = user.telegram_id, keyboard = keyboard)
        
        if isinstance(self.media, list):
            return await self._send_post_media_group(chat_id = user.telegram_id, keyboard = keyboard) 
        
        if self.media.file_type == MediaTypeEnum.PHOTO:
            return await self._send_post_photo(chat_id = user.telegram_id, keyboard = keyboard)
        
        if self.media.file_type == MediaTypeEnum.VIDEO:
            return await self._send_post_video(chat_id = user.telegram_id, keyboard = keyboard)


    @log_exceptions      
    async def _send_post_media_group(self, chat_id: int, keyboard: InlineKeyboardMarkup): 
        media_group = MediaGroupBuilder(caption = self.post.text)
        for current_media in self.media:
            media_group.add(
                type  = current_media.file_type.value.lower(),
                media = FSInputFile(
                    path     = self.patch_path(current_media.file_url),
                    filename = current_media.file_url.split("/")[-1]        
                                    )
            )
            
        message_grouped = await self.bot.send_media_group(
            chat_id = chat_id,
            media   = media_group.build()
        )
        await self.bot.send_message(chat_id = chat_id,
                                    text   = "Опубликовать пост?",
                                    reply_markup = keyboard,
                                    reply_to_message_id = message_grouped[0].message_id)
    
    @log_exceptions
    async def _send_post_video(self, chat_id: int, keyboard: InlineKeyboardMarkup):
        video = FSInputFile(
            path     = self.patch_path(self.media.file_url), 
            filename = self.media.file_url.split("/")[-1]
                        )
        
        await self.bot.send_video(
            chat_id      = chat_id,
            video        = video,
            caption      = self.post.text,
            reply_markup = keyboard            
        )

            
    @log_exceptions
    async def _send_post_photo(self, chat_id: int, keyboard: InlineKeyboardMarkup):
        
        photo = FSInputFile(
            path     = self.patch_path(self.media.file_url), 
            filename = self.media.file_url.split("/")[-1]
                        )
        
        await self.bot.send_photo(
            chat_id      = chat_id,
            photo        = photo,
            caption      = self.post.text,
            reply_markup = keyboard
                                )   

    @log_exceptions
    async def _send_post_message(self, chat_id: int, keyboard: InlineKeyboardMarkup):
        await self.bot.send_message(
            chat_id=chat_id,
            text=self.post.text,
            reply_markup=keyboard
                                    )
