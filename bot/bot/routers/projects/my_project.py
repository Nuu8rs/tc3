from aiogram import Router, F
from aiogram.types import  CallbackQuery, Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.fsm.context import FSMContext

from database.models.users import User
from database.models.chats import ProjectChatAssociation
from database.models.projects import Project

from bot.services.project_service import ProjectService
from bot.services.project_chat_association_service import ProjceChatAssociationService

from bot.bot.filters.clear_filter import ClearFilter
from bot.bot.callbacks.project_callbacks import SelectProject

from bot.bot.keyboard.project_keyboard import select_options_project

from bot.bot.states.bot_chat_state import AddBotToChat

from bot.bot.keyboard.project_keyboard import (my_projects_keyboard, 
                                           create_project_keyboard,
                                           select_chat_from_create_project_keyboard)

my_project_router = Router()

# #TODO ONLY SUBSCRIBE

@my_project_router.message(F.text == __("Мои проекты"), ClearFilter()) # TODO CHECKER SUBSC
async def my_project_handler(message: Message, user: User):
    projects = await ProjectService.get_projects_from_user(id_user=user.id)
    
    if not projects:
        await message.answer(_("У вас нету проектов, вы можете создать его"),
                             reply_markup = create_project_keyboard()
                             ) 
    else:
        await message.answer(_("Твои проекты"),
                             reply_markup = my_projects_keyboard(projects=projects)
                             )


    
@my_project_router.callback_query(F.data == "create_project")
async def create_project_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(AddBotToChat.add_bot)
    await query.message.answer(_("Выберите чат в который приходить посты, по данному проекту"),
                               reply_markup=select_chat_from_create_project_keyboard())
    
    


@my_project_router.callback_query(SelectProject.filter(), ClearFilter())
async def select_project(query: CallbackQuery, user: User, callback_data: SelectProject):
    project: Project = await ProjectService.get_project(
        project_id=callback_data.project_id
    )
    if not project:
        return await query.answer("Не найденно проекта", show_alert=True)
    
    project_association: list[ProjectChatAssociation] = await ProjceChatAssociationService.get_association_by_project_id(
        project_id=project.id
    )
    
    text = f"""
Ваш проект - {project.chat_name}

Кол-во чатов - {len(project_association)}
"""

    await query.message.answer(
        text = text,
        reply_markup = select_options_project(
            project_id=project.id
        )
    )