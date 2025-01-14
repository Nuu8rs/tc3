from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import User as UserBot

from .storage import get_state_data

from database.models.users import User

from bot.services.user_service import UserService


async def get_user(user_bot: UserBot, state: FSMContext) -> User:
    
    user = await get_state_data(state, "user")
    
    if not user:
        
        user = await UserService.get_user_by_user_id(user_id = user_bot.id)
        if not user:
            
            user = await UserService.create_user(
                full_name = user_bot.full_name,
                user_name = user_bot.username,
                user_id   = user_bot.id,
                language  = user_bot.language_code
            )
            
    return user
