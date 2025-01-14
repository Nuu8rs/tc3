from aiogram import Router
from aiogram.types import Message
from bot.bot.filters.chat_project_filter import ChatProjectFilter

post_editer_description_router = Router()

@post_editer_description_router.message(ChatProjectFilter())
async def add_describe_to_message_handler(message: Message):
    curr_message = message
    await message.delete()
    text_description = "\n\nПодписаться"
    new_message = await curr_message.send_copy(
        chat_id = message.chat.id,
    )
    await message.bot.edit_message_text(
        chat_id = message.chat.id,
        text = (new_message.html_text + text_description),
        message_id = new_message.message_id
    )