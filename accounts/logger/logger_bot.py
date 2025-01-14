import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from accounts.config import LOGGER_CHAT_ID, BOT_TOKEN_LOGGER_BOT

from logging import Handler





class TelegramHandler(Handler):
    sleep_time = 0.3
    topics_id = {
        "INFO"     : 522,
        "WARNING"  : 526,
        "ERROR"    : 524
    }    
    
    
    
    async def send_log(self, message: str, level_name: str):
        await asyncio.sleep(self.sleep_time)
        try:
            ...   
            # await logger_bot.send_message(
            #     chat_id=LOGGER_CHAT_ID, 
            #     text=message,
            #     message_thread_id=self.topics_id[level_name]
            #     )
            
        except Exception as e:
            print(f"Failed to send log to Telegram: {e}")

    def emit(self, record):
        log_entry = self.format(record)
        level_name = record.levelname
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_log(log_entry, level_name)) 

logger_bot = Bot(BOT_TOKEN_LOGGER_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))