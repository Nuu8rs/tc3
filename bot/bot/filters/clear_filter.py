from typing import Any
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

class ClearFilter(BaseFilter):
    
    async def __call__(self, event: Message, state: FSMContext, *args: Any, **kwds: Any) -> Any:
        state_user = await state.get_state()
        if state_user:
            await state.clear()
            await event.answer("Ваш стейт был очищен, если вы что-то вводили, введите еще раз")
        
        return True