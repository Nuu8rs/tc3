from aiogram import Router
from aiogram.types import  CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.api.teletracker_accounts.teletracker_api import DeleteChatViews
from bot.api.schemas import BaseResponse

from bot.bot.filters.clear_filter import ClearFilter
from bot.bot.callbacks.project_callbacks import DeleteProjectChat

from bot.services.project_chat_association_service import ProjceChatAssociationService

delete_chat_from_project_router = Router()

@delete_chat_from_project_router.callback_query(DeleteProjectChat.filter(), ClearFilter())
async def delete_chat_from_project_handker(query: CallbackQuery, callback_data: DeleteProjectChat):
    await ProjceChatAssociationService.delete_chat_from_project(
        project_id = callback_data.project_id,
        chat_id    = callback_data.chat_id
    )
    delete_chat_views_api =  DeleteChatViews(chat_id = callback_data.chat_id)
    
    response: BaseResponse = await delete_chat_views_api.send_response()
    
    if not response.is_succes:
        return await query.message.answer("Произошла ошибка, попробуйте позже")
    
    await query.message.edit_text(_("Вы удалили чат"), reply_markup = None)