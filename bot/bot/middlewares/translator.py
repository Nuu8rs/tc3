
from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18n
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n.middleware import FSMI18nMiddleware
from bot.bot.functions.storage import get_state_data

from bot.services.user_service import UserService
from database.models.users import User
from bot.loader import dp
from typing import Any, Dict

class CustomI18nMiddleware(FSMI18nMiddleware):
    
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        state: FSMContext = data.get("state")
        locale = None
        if state:
            locale = await get_state_data(state, "locale")
            
        if not locale:
            if hasattr(event, "from_user") and event.from_user:
                user: User = await UserService.get_user_by_user_id(user_id = event.from_user.id)
                if user:
                    locale = user.language
                else:
                    locale = await super().get_locale(event=event, data=data)
            else:
                locale = await super().get_locale(event=event, data=data)
            if state and locale:
                await state.update_data(data={self.key: locale})
        return locale

    async def set_locale(self, state, locale) -> str:
        await state.update_data(data={self.key: locale})
        self.i18n.current_locale = locale
        
    def set_locale_no_state(self, locale) -> str:
        self.i18n.current_locale=locale

i18n = I18n(path="bot/locales", default_locale="ru", domain="messages")
i18n_middleware = CustomI18nMiddleware(i18n=i18n)
i18n_middleware.setup(dp)