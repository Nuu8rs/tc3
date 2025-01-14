import asyncio
from aiohttp import web

from database.models.base_accessor import get_base 
from accounts.session import engine


from accounts.loader import  account_manager, account_validator, runner
from accounts.logger.logger import logger
from accounts.config import WEBAPP_HOST, WEBAPP_PORT

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(get_base().metadata.create_all)

async def start_accounts_work():
    logger.info("НАЧАЛО ИНИЦИАЛИЗАЦИИ АККАУНТОВ")
    await account_manager.starting_accounts()
    asyncio.create_task(account_validator.start_validation())
    logger.info("ИНИЦИАЛИЗАЦИя АККАУНТОВ УСПЕШНА")


async def init_account_bots():
    try:
        await start_accounts_work()
        await asyncio.Event().wait()
    except Exception as E:
        logger.error(E)

async def start_webhook():
    logger.info("НАЧАЛО ИНИЦИАЛИЗАЦИИ ВЕБХУКА")
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)
    await site.start()
    logger.info("ИНИЦИАЛИЗАЦИЯ ВЕБХУКА УСПЕШНА")

async def main():
    await init_db()
    logger.info("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ПРОШЛА УСПЕШНО")

    await asyncio.gather(
        start_webhook(),
        init_account_bots()
    )
        
    

        
if __name__ == "__main__":
    asyncio.run(main())