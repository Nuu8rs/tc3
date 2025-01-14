import random
from aiogram.types import ChatAdministratorRights, KeyboardButtonRequestChat

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from database.models.projects import Project
from database.models.chats import Chat
from database.models.chats import ProjectChatAssociation

from bot.bot.types import StatusAutopost

from bot.bot.keyboard.utils_keyboard import pagination_keyboard

from bot.bot.callbacks.switcher import (
    SwitchProject,
    SwitchChatsProject
                                    )
from bot.bot.callbacks.project_callbacks import (
    AskDeleteProject,
    SelectProject,
    DeleteProject,
    ViewChatProject,
    AddChatToProject,
    SelectChatProject,
    DeleteProjectChat,
    EditStatusAutopost
                                            ) 

from bot.constans import ELEMENT_PER_PAGE

#TODO user: User, subscription_user: Subscription
def create_project_keyboard(attach: bool = False):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text = _("Создать проект"),
        callback_data="create_project"
    )
    if attach:
        return keyboard
    
    return keyboard.adjust(1).as_markup()


def my_projects_keyboard(projects: list[Project], page: int = 0):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.attach(pagination_keyboard(
        current_page=page,
        total_items=len(projects),
        switcher=SwitchProject
    ))
    
    start = page * ELEMENT_PER_PAGE
    end = start + ELEMENT_PER_PAGE
    project_in_page = projects[start:end]
    
    for project in project_in_page:
        keyboard.button(
            text          = project.chat_name,
            callback_data = SelectProject(
                project_id=project.id
            )
        )
    
    keyboard.attach(create_project_keyboard(attach=True))
    
    len_models_page = len(project_in_page)
    limit_butt_line = 3
        
    ostacha = len_models_page%limit_butt_line
    last = [3, ostacha] if ostacha else [3]
    keyboard.adjust(*( [3]*(len_models_page//limit_butt_line)), *last, 1)
    return keyboard.as_markup()


def select_chat_from_create_project_keyboard(random_id=random.randrange(111100000, 111199999)):
    return (ReplyKeyboardBuilder()
        .button(
            text=_("Добавить группу"),
            request_chat=KeyboardButtonRequestChat(
                user_administrator_rights=ChatAdministratorRights(
                    is_anonymous=False,
                    can_manage_video_chats=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_restrict_members=True,
                    can_manage_chat=True,
                    can_promote_members=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_pin_messages=True,
                    can_manage_topics=True,
                    can_post_stories=False,         
                    can_edit_stories=False,         
                    can_delete_stories=False        
                ),
                bot_administrator_rights=ChatAdministratorRights(
                    is_anonymous=False,
                    can_manage_video_chats=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_manage_chat=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_pin_messages=True,
                    can_manage_topics=True,
                    can_post_stories=False,         
                    can_edit_stories=False,         
                    can_delete_stories=False        
                ),
                request_id=random_id,
                chat_is_channel=False,
                chat_is_forum=False,
            )
        )
        .button(
            text=_("Добавить форум"),
            request_chat=KeyboardButtonRequestChat(
                user_administrator_rights=ChatAdministratorRights(
                    is_anonymous=False,
                    can_manage_video_chats=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_restrict_members=True,
                    can_manage_chat=True,
                    can_promote_members=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_pin_messages=True,
                    can_manage_topics=True,
                    can_post_stories=False,         
                    can_edit_stories=False,         
                    can_delete_stories=False        
                ),
                bot_administrator_rights=ChatAdministratorRights(
                    is_anonymous=False,
                    can_manage_video_chats=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_manage_chat=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_pin_messages=True,
                    can_manage_topics=True,
                    can_post_stories=False,         
                    can_edit_stories=False,         
                    can_delete_stories=False        
                ),
                request_id=random_id + 1,
                chat_is_channel=False,
                chat_is_forum=True,
            )
        )
        .button(
            text=_("Добавить канал"),
            request_chat=KeyboardButtonRequestChat(
                user_administrator_rights=ChatAdministratorRights(
                    is_anonymous=False,
                    can_manage_video_chats=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_restrict_members=True,
                    can_manage_chat=True,
                    can_promote_members=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_pin_messages=True,
                    can_manage_topics=True,
                    can_post_stories=False,         
                    can_edit_stories=False,         
                    can_delete_stories=False        
                ),
                bot_administrator_rights=ChatAdministratorRights(
                    is_anonymous=False,
                    can_manage_video_chats=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_manage_chat=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_pin_messages=True,
                    can_manage_topics=True,
                    can_post_stories=False,         
                    can_edit_stories=False,         
                    can_delete_stories=False        
                ),
                request_id=random_id + 2,
                chat_is_channel=True,
                chat_is_forum=False,
            )
        )
        .adjust(1)
        .as_markup()
    )


def select_options_project(project_id: int):
    return (
        InlineKeyboardBuilder()
        .button(text = "Удалить проект", 
                callback_data = AskDeleteProject(
                    project_id=project_id
                                             )
                )
        .button(text = "Просмотр чатов проекта", 
                callback_data = ViewChatProject(
                    project_id = project_id
                                               )
                )
        .button(text = "Добавить чат", 
                callback_data = AddChatToProject(
                    project_id = project_id
                                                )
                )
        .adjust(1)
        .as_markup()
    )
    
    
def views_chats_project_keyboard(chats: list[Chat], project_id: int, page: int = 0):
    keyboard = InlineKeyboardBuilder()
    keyboard.attach(pagination_keyboard(
        current_page=page,
        total_items=len(chats),
        switcher=SwitchChatsProject
    ))
    
    start = page * ELEMENT_PER_PAGE
    end = start + ELEMENT_PER_PAGE
    
    chats_in_page = chats[start:end]
    
    for chat in chats_in_page:
        keyboard.button(
            text= chat.chat_name,
            callback_data= SelectChatProject(
                chat_id=chat.chat_id,
                project_id=project_id
            )
        )
        
    len_item_in_page = len(chats_in_page)
    limit_butt_line = 2
        
    ostacha = len_item_in_page%limit_butt_line
    last = [limit_butt_line, ostacha] if ostacha else [limit_butt_line]
    keyboard.adjust(3, *([limit_butt_line]*(len_item_in_page//limit_butt_line)), *last)
    return keyboard.as_markup()


def chat_project_options_keyboard(project_chat_association: ProjectChatAssociation):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text          = "Удалить чат",
        callback_data = DeleteProjectChat(
            chat_id    = project_chat_association.chat_id,
            project_id = project_chat_association.project_id
        )
    )
    
    if not project_chat_association.auto_post:
        text_autopost = "Включить авто постинг"
        status_autopost = StatusAutopost.TURN_AUTOPOST.value
    else:
        text_autopost = "Отключить автопостинг"
        status_autopost = StatusAutopost.DISABLE_AUTUPOST.value
    
    keyboard.button(
        text          = text_autopost,
        callback_data = EditStatusAutopost(
            chat_id         = project_chat_association.chat_id,
            project_id      = project_chat_association.project_id,
            status_autopost = status_autopost
                                            )
                    )
    return keyboard.adjust(1).as_markup()


def ask_for_delete_project(project_id: int):
    return (
        InlineKeyboardBuilder()
        .button(text = _("Да удалить"),
                callback_data = DeleteProject(
                    project_id=project_id
                ))
        .button(text = _("Отменить"), callback_data="delete_message")
        .adjust(1)
        .as_markup()
    )
