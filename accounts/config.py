from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv
import os


load_dotenv()

WEBAPP_HOST = os.getenv("WEBAPP_HOST")
WEBAPP_PORT = os.getenv("WEBAPP_PORT")

BOT_TOKEN_LOGGER_BOT = os.getenv("BOT_TOKEN_LOGGER_BOT")
LOGGER_CHAT_ID       = int(os.getenv("LOGGER_CHAT_ID"))

BOT_TOKEN_TELETRACKER = os.getenv("BOT_TOKEN")

class DatabaseConfig:
    _url_conntect_db = os.getenv("ASYNC_DATABASE_URL")
    

    @classmethod
    def get_connection_string(cls) -> str:
        return cls._url_conntect_db
    
bot_teletracker = Bot(token=BOT_TOKEN_TELETRACKER, default=DefaultBotProperties(parse_mode=ParseMode.HTML))