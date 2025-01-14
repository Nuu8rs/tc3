from aiogram.filters.state import State, StatesGroup

class AddBotToChat(StatesGroup):
    add_bot = State()