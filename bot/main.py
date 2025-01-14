import asyncio
from aiohttp import web

import bot.bot.middlewares
from bot.bot.routers.router import main_router
from bot.loader import bot, dp, init_db

from bot.loader import runner
from bot.config import config

from bot.logger.logger import logger

dp.include_router(main_router)


async def start_polling():
    await dp.start_polling(bot)

async def main():
    await init_db()
    await asyncio.gather(
        start_polling(),
        start_webhook()
    )
    

async def start_webhook():
    logger.info("НАЧАЛО ИНИЦИАЛИЗАЦИИ ВЕБХУКА")
    await runner.setup()
    site = web.TCPSite(
        runner, 
        config.webhook_api.WEBAPP_HOST, 
        config.webhook_api.WEBAPP_BOT_PORT)
    await site.start()
    logger.info("ИНИЦИАЛИЗАЦИЯ ВЕБХУКА УСПЕШНА")

    
if __name__ == "__main__":
    asyncio.run(main())
