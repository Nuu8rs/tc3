from aiogram import Router

from .commands.router import commands_router
from .projects.router import project_router
from .bot_functional_chat.router import bot_chat_router
from .posts.router import post_router

main_router = Router()

main_router.include_routers(
    commands_router,
    bot_chat_router,
    project_router,
    post_router
)