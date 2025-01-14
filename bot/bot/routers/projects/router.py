from aiogram import Router
from .my_project import my_project_router
from .project_functional.add_account_to_chat import add_chat_to_project_router
from .project_functional.functional_chats_project import functional_chats_project_router
from .project_functional.delete_chat_from_project import delete_chat_from_project_router
from .project_functional.delete_project import delete_project_router

project_router = Router()

project_router.include_routers(
    my_project_router,
    add_chat_to_project_router,
    functional_chats_project_router,
    delete_chat_from_project_router,
    delete_project_router
)