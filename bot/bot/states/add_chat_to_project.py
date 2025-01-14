from aiogram.filters.state import State, StatesGroup

class AddChatToProjectState(StatesGroup):
    send_chat_link = State()