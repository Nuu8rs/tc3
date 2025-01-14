from aiogram import Router
from aiogram.types import  CallbackQuery, Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.fsm.context import FSMContext

from bot.api.teletracker_accounts.teletracker_api import AddChatToAccount
from bot.api.schemas import ResponseAddAccount

from bot.services.project_chat_association_service import ProjceChatAssociationService

from bot.bot.filters.clear_filter import ClearFilter
from bot.bot.functions.project_utils import is_telegram_chat_link
from bot.bot.callbacks.project_callbacks import AddChatToProject

from bot.bot.states.add_chat_to_project import AddChatToProjectState

add_chat_to_project_router = Router()

@add_chat_to_project_router.callback_query(AddChatToProject.filter(), ClearFilter())
async def add_chat_to_project(query: CallbackQuery, callback_data: AddChatToProject, state: FSMContext):
    await query.message.answer("Введите ссылку на чат ")
    await state.update_data(project_id = callback_data.project_id)
    await state.set_state(AddChatToProjectState.send_chat_link)
    

    
@add_chat_to_project_router.message(AddChatToProjectState.send_chat_link)
async def send_chat_link(message: Message, state: FSMContext):
    if not is_telegram_chat_link(message.text):
        return await message.answer(_("Введите корректную ссылку на чат"))
    
    data = await state.get_data()
    project_id = data.get("project_id", False)
    
    
    if not project_id:
        return await message.answer("Введите корректную ссылку")
    
    await message.answer(_("Начинаю подключение к чату"))
    add_chat_to_account = AddChatToAccount(
        chat_link  = message.text,
        project_id = project_id
    )
    
    result_join_account_to_chat:ResponseAddAccount = await add_chat_to_account.send_response()
    
    await message.answer(
        text = result_join_account_to_chat.message_join_result.format(
            chat_link = message.text
        )
    )
    await state.clear()
    