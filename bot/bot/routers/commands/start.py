from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from database.models.users import User

from bot.bot.keyboard.main_keyboard import main_keyboard
from bot.bot.filters.clear_filter import ClearFilter


start_router = Router()

@start_router.message(CommandStart(), ClearFilter())
async def start_handler(message: Message, state: FSMContext, user: User):
    await message.answer(text = "Мейн меню",
                         reply_markup = main_keyboard())