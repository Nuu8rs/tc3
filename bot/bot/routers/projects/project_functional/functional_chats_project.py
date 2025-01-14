from aiogram import Router
from aiogram.types import  CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from database.models.chats import Chat
from database.models.chats import ProjectChatAssociation

from bot.services.project_chat_association_service import ProjceChatAssociationService
from bot.services.chat_service import ChatService

from bot.bot.callbacks.project_callbacks import ViewChatProject, SelectChatProject, DeleteProjectChat, EditStatusAutopost
from bot.bot.keyboard.project_keyboard import views_chats_project_keyboard, chat_project_options_keyboard

functional_chats_project_router = Router()

  
@functional_chats_project_router.callback_query(ViewChatProject.filter())
async def views_chats_project_handler(query: CallbackQuery, callback_data: ViewChatProject):
    all_chats_project_association: list[ProjectChatAssociation] = await ProjceChatAssociationService.get_association_by_project_id(
        project_id=callback_data.project_id
    )
    chats_id = [chat_assoc.chat_id for chat_assoc in all_chats_project_association]
    all_chats_from_project: list[Chat] = await ChatService.get_chats(
        chats_id = chats_id  
    )
    
    await query.message.answer(
        text="Ваши чаты по проекту",
        reply_markup = views_chats_project_keyboard(
            chats = all_chats_from_project,
            project_id = callback_data.project_id 
        )
    )
    

@functional_chats_project_router.callback_query(SelectChatProject.filter())
async def view_chat_project_handler(query: CallbackQuery, callback_data: SelectChatProject, _edit: bool = False):
    chat: Chat = await ChatService.get_chat(chat_id=callback_data.chat_id)
    if not chat:
        return
    
    project_chat_association:ProjectChatAssociation = await ProjceChatAssociationService.get_chat_association(
        chat_id=chat.chat_id,
        project_id=callback_data.project_id
    ) 
    if not project_chat_association:
        return
    
    autopost_text = "Посты с данного чата будут приходить в бота: " + ("✅" if project_chat_association.auto_post else "❌") 
    
    text_chat = f"""
Чат - {chat.chat_name}
ID - {chat.chat_id}
Link connect - {chat.chat_link}

{autopost_text}
            """
    
    keyboard =  chat_project_options_keyboard(project_chat_association)
    
    if _edit:
        await query.message.edit_text(
            text         = text_chat,
            reply_markup = keyboard
        )
    else:  
        await query.message.answer(
            text         = text_chat,
            reply_markup = keyboard
        )
    
@functional_chats_project_router.callback_query(EditStatusAutopost.filter())
async def edit_status_project_chat_autopost_handler(query: CallbackQuery, callback_data: EditStatusAutopost):
    await ProjceChatAssociationService.edit_status_autopost(
        chat_id          = callback_data.chat_id,
        project_id       = callback_data.project_id,
        status_auto_post = callback_data.status_autopost
    )
    return await view_chat_project_handler(
        query = query,
        callback_data = SelectChatProject(
            chat_id    = callback_data.chat_id,
            project_id = callback_data.project_id
        ),
        _edit = True
    )
