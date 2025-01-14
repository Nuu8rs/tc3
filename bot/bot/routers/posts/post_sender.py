from aiogram import Router, F
from aiogram.types import  CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.bot.functions.sender_message_post import SenderPostsToProject

from database.models.projects import Project
from database.models.posts import Post, Media

from bot.services.project_service import ProjectService
from bot.services.post_service import PostService
from bot.services.media_service import MediaService


from bot.bot.filters.clear_filter import ClearFilter
from bot.bot.callbacks.post_callbacks import SendPostToProject

sender_post_router = Router()

@sender_post_router.callback_query(SendPostToProject.filter(),ClearFilter())
async def send_post_to_project(query: CallbackQuery, callback_data: SendPostToProject):
    project: Project = await ProjectService.get_project(project_id = callback_data.project_id)
    if not project:
        return await query.answer(_("Не смог найти проект"), show_alert= True)
    post: Post = await PostService.get_post(post_id = callback_data.post_id)
    if not post:
        return await query.answer(_("Не смог найти пост"), show_alert= True)
    
    media: Media | list[Media] = await MediaService.get_media_to_post(
        post_id = callback_data.post_id
    )
    
    post_sender = SenderPostsToProject(
        post    = post,
        project = project,
        media   = media
    )
    await post_sender.send_message()