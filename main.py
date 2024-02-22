import logging

import coloredlogs

from src.bot import Bot
from src.core.config import Config

coloredlogs.install(level=logging.INFO, fmt="%(asctime)s %(name)s %(levelname)s: %(message)s")
logger = logging.getLogger("Main")

if __name__ == '__main__':
    config = Config()
    log_level = config.get("bot.log_level", "INFO")
    coloredlogs.set_level(log_level)
    bot = Bot(config)
    try:
        bot.start()
    except KeyboardInterrupt:
        logger.info("Exiting...")
        exit(0)
