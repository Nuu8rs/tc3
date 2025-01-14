from aiogram import Router

from .add_bot_to_chat import add_bot_to_chat_router
from .post_descibtion import post_editer_description_router


bot_chat_router = Router()
bot_chat_router.include_routers(
    add_bot_to_chat_router,
    post_editer_description_router
)