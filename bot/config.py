import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from pydantic import Field
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()

class BotConfig(BaseSettings):
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")

    @property
    def BOT_ID(self) -> int:
        return int(self.BOT_TOKEN.split(":")[0])

# Конфигурация логгера бота
class BotLoggerConfig(BaseSettings):
    LOGGER_CHAT_ID: int = Field(..., env="LOGGER_CHAT_ID")
    BOT_TOKEN_LOGGER_BOT: str = Field(..., env="BOT_TOKEN_LOGGER_BOT")


# Конфигурация базы данных
class DataBaseConfig(BaseSettings):
    @property
    def master_key_connect(self) -> str:
        return os.getenv("ASYNC_DATABASE_URL")


class WebhookApi(BaseSettings):
    WEBAPP_HOST: str = Field(..., env="WEBAPP_HOST")
    WEBAPP_BOT_PORT: int =  Field(..., env="WEBAPP_BOT_PORT")

# Общий класс конфигурации
class Config:
    def __init__(self):
        self.webhook_api = WebhookApi()
        self.AUTH_SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY") 
        self.BASE_API_URL: str = os.getenv("BASE_API_URL")
        self.bot_config        = BotConfig()
        self.bot_logger_config = BotLoggerConfig()
        self.database_config   = DataBaseConfig()

config = Config()

bot_logger = Bot(token=config.bot_logger_config.BOT_TOKEN_LOGGER_BOT, 
                   default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    