from aiogram.utils.keyboard import ReplyKeyboardBuilder, WebAppInfo
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from database.models.users import User
from database.models.subscriptions import Subscription


#TODO user: User, subscription_user: Subscription
def main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.button(text = _("Мои проекты"))
    return keyboard.adjust(1).as_markup()