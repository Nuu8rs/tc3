from aiogram.filters.callback_data import CallbackData
from bot.bot.types import StatusAutopost

class SelectProject(CallbackData, prefix = "select_project"):
    project_id: int
    
class AskDeleteProject(CallbackData, prefix = "ask_delete_project"):
    project_id: int

class DeleteProject(CallbackData, prefix = "delete_project"):
    project_id: int
    
class ViewChatProject(CallbackData, prefix = "view_chats"):
    project_id: int
    
class AddChatToProject(CallbackData, prefix = "add_chat_to_project"):
    project_id: int
    
class SelectChatProject(CallbackData, prefix = "select_chat_project"):
    chat_id: int
    project_id: int
    
class DeleteProjectChat(CallbackData, prefix = "delete_project_chat"):
    chat_id: int
    project_id: int
    
class EditStatusAutopost(CallbackData, prefix = "edit_autopost"):
    chat_id: int
    project_id: int
    status_autopost: bool