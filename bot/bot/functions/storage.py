from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.loader import dp
from bot.config import config

def get_custom_storage_key(key: StorageKey, new_user_id) -> StorageKey:
    return StorageKey(bot_id=key.bot_id, chat_id=key.chat_id, user_id=new_user_id, thread_id=key.thread_id, destiny=key.destiny)

def get_target_state(state: FSMContext, userid: int) -> FSMContext:
    return FSMContext(storage=dp.storage, key=get_custom_storage_key(state.key, userid))

def get_state_by_user(user_id: int) -> FSMContext:
    storage = StorageKey(
        bot_id = config.bot_config.BOT_ID,
        chat_id=user_id,
        user_id=user_id,
    )
    return FSMContext(
        storage=dp.storage,
        key=storage
    )

async def get_state_data(state: FSMContext, key: str, userid: int = 0, default=None) -> Any:
    if userid:
        state = get_target_state(state, userid)
    state_data = await state.get_data()
    if key in state_data:
        return state_data[key]
    return default