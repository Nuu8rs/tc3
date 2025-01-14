import stat
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER, IS_ADMIN, PROMOTED_TRANSITION
from aiogram.methods import SendMessage
from aiogram.utils.i18n import gettext as _
from aiogram.types import ChatMemberUpdated

from bot.bot.states.bot_chat_state import AddBotToChat
from bot.bot.keyboard.main_keyboard import main_keyboard

from bot.bot.functions.bot_chat_func import admin_rights_list, check_all_admin_rights, get_admin_rights
from bot.bot.functions.storage import get_state_by_user

from bot.services.project_service import ProjectService
from bot.services.user_service import UserService

add_bot_to_chat_router = Router()

@add_bot_to_chat_router.my_chat_member(ChatMemberUpdatedFilter(IS_ADMIN))
async def on_bot_promote(event: ChatMemberUpdated):
    try:
        await event.bot.send_message(event.from_user.id, _("Начинаю проверку. . ."))
    except TelegramForbiddenError:
        return SendMessage(chat_id=event.chat.id, text=_("Добавьте меня через интерфейс бота или отключите анонимность чтобы я мог определить вас как администратора"))
    
    state: FSMContext = get_state_by_user(user_id = event.from_user.id)
    current_state = await state.get_state()
    
    if not current_state or current_state != AddBotToChat.add_bot:
        return await event.bot.leave_chat(event.chat.id)


    if not check_all_admin_rights(event.new_chat_member, admin_rights_list[event.chat.type]):
        await event.bot.leave_chat(event.chat.id)
        return SendMessage(chat_id=event.from_user.id, text=_("У меня недостаточно прав в чате [{title}]").format(title=event.chat.full_name))

    #TODO ПРОВЕРКА ПОДПИСКИ
    # if not await users_db.has_subscription(userid=message.chat.id):
    #     await event.bot.leave_chat(event.chat.id)
    #     return SendMessage(chat_id=event.from_user.id, text=_("У вас истек срок действия подписки, часть моих функций будет недоступна до возобновления подписки."))
    #TODO ПРОВЕРКА ТОГО ЧТО ЧАТ НЕ ЗАНЯТ
    # if not (await contest_db.create_channel_owner(event)):
    #     await event.bot.leave_chat(event.chat.id)
    #     return SendMessage(chat_id=event.from_user.id, text=_("Этот чат уже был добавлен другим пользователем").format(title=event.chat.full_name))
    user = await UserService.get_user_by_user_id(user_id = event.from_user.id)
    await ProjectService.add_new_project(
        id_user   = user.id,
        chat_id   = event.chat.id,
        chat_name = event.chat.full_name
    )
    return SendMessage(chat_id=event.from_user.id, 
                       text=_("✅ <b>Бот был добавлен в</b> [{title}] и готов постить").format(title=event.chat.full_name),
                       reply_markup=main_keyboard()
                       )
    
#TODO СДЕЛАТЬ КУЧА ПРОВЕРОК
# @add_bot_to_chat_router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
# async def on_bot_leave(event: ChatMemberUpdated):
#     await channels_db.delete_channel(event.chat.id, event.bot.token)
#     return SendMessage(chat_id=event.from_user.id, text=_("Я не могу выполнять свои функции в чате [{title}] так как меня удалили").format(title=event.chat.full_name))

# @add_bot_to_chat_router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def on_bot_join(event: ChatMemberUpdated):
#     return SendMessage(chat_id=event.from_user.id, text=_("Мне нужны права администратора в этом чате [{title}]").format(title=event.chat.full_name))

# @add_bot_to_chat_router.my_chat_member(ChatMemberUpdatedFilter(~PROMOTED_TRANSITION))
# async def on_bot_restrict(event: ChatMemberUpdated):
#     await channels_db.update_channel_rights(event.chat.id, event.new_chat_member.status == "administrator", get_admin_rights(event.new_chat_member, admin_rights_list[event.chat.type]), event.bot.token)
#     return SendMessage(chat_id=event.from_user.id, text=_("Пожалуйста, верните права администратора в чате [{title}]").format(title=event.chat.full_name))
