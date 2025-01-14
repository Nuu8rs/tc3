from aiogram import Router, F
from aiogram.types import  CallbackQuery

from bot.bot.filters.clear_filter import ClearFilter
from bot.bot.callbacks.post_callbacks import DeletePostProject

delete_message_post_router = Router()

@delete_message_post_router.callback_query(DeletePostProject.filter(), ClearFilter())
async def delete_message_post_handler(query: CallbackQuery):
    await query.message.delete()