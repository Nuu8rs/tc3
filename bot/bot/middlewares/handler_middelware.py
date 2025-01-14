
from aiogram.types import Message, CallbackQuery
from bot.bot.functions.middelwate_func import get_user
from database.models.users import User

from typing import Any, Awaitable, Callable, Dict
from bot.loader import dp

@dp.callback_query.outer_middleware()
@dp.message.outer_middleware()
async def message_middleware(
    handler: Callable[[Message|CallbackQuery, Dict[str, Any]], Awaitable[Any]],
    event: Message|CallbackQuery,
    data: Dict[str, Any]
) -> Any:
    if isinstance(event, CallbackQuery):
        await event.answer()
    
    user: User = await get_user(user_bot = event.from_user, state = data.get("state"))
    data.update({"user":user})
    result = await handler(event, data)
    return result