import asyncio
from bot.config import config, bot_logger

from logging import Handler





class TelegramHandler(Handler):
    sleep_time = 0.3
    topics_id = {
        "INFO"     : 522,
        "WARNING"  : 526,
        "ERROR"    : 524
    }    
    prefix_log = "[BOT TELETRACKER] "
    
    
    async def send_log(self, message: str, level_name: str):
        await asyncio.sleep(self.sleep_time)
        try:
            
            await bot_logger.send_message(
                chat_id           = config.bot_logger_config.LOGGER_CHAT_ID, 
                text              = self.prefix_log + message.replace("<","").replace(">",""),
                message_thread_id = self.topics_id[level_name]
                )
            
        except Exception as e:
            print(f"Failed to send log to Telegram: {e}")

    def emit(self, record):
        log_entry = self.format(record)
        level_name = record.levelname
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_log(log_entry, level_name)) 
