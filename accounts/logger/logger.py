import logging
from colorlog import ColoredFormatter
from .logger_bot import TelegramHandler

class LoggerConfig:
    @staticmethod
    def setup_logger():
        color_format = (
            '%(log_color)s%(asctime)s | %(levelname)-5s | %(filename)-14s | %(funcName)-10s | %(message)s%(reset)s'
        )

        formatter = ColoredFormatter(
            fmt=color_format,
            datefmt='%Y-%m-%d %H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        telegram_handler = TelegramHandler()
        telegram_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S'))

        logging.basicConfig(level=logging.INFO, handlers=[handler, telegram_handler], force=True)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
    
LoggerConfig.setup_logger()
logger = LoggerConfig.get_logger(__name__)