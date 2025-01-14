from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.models.base_accessor import get_base 

from bot.session import engine
from bot.webhook_api.handlers import SendPostHandler

from bot.config import config

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(get_base().metadata.create_all)
        
def add_web_endoints():
    application.router.add_post("/sendPost", handler = SendPostHandler.router)

bot = Bot(token=config.bot_config.BOT_TOKEN, 
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()


application = web.Application()
runner = web.AppRunner(application)

add_web_endoints()
