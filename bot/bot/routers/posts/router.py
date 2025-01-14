from aiogram import Router
from .post_sender import sender_post_router
from .post_delete_message import delete_message_post_router

post_router = Router()


post_router.include_routers(
    sender_post_router,
    delete_message_post_router
)