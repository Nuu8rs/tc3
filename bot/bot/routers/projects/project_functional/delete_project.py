from aiogram import Router
from aiogram.types import  CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.api.schemas import BaseResponse

from bot.bot.callbacks.project_callbacks import DeleteProject, AskDeleteProject
from bot.bot.keyboard.project_keyboard import ask_for_delete_project
from bot.bot.filters.clear_filter import ClearFilter

from bot.services.project_chat_association_service import ProjceChatAssociationService
from bot.services.project_service import ProjectService


delete_project_router = Router()

@delete_project_router.callback_query(AskDeleteProject.filter(), ClearFilter())
async def ask_delete_project_handler(query: CallbackQuery, callback_data: AskDeleteProject):
    await query.message.edit_text(
        text         = _("Вы точно хотите удалить проект?"),
        reply_markup = ask_for_delete_project(
            project_id= callback_data.project_id
        )
    )
    

@delete_project_router.callback_query(DeleteProject.filter(), ClearFilter())
async def delete_project_handler(query: CallbackQuery, callback_data: DeleteProject):
    await ProjceChatAssociationService.delete_association_from_project(project_id=callback_data.project_id)
    await ProjectService.delete_project(project_id=callback_data.project_id)
    await query.message.edit_text(_("Вы удалили свой проект"))