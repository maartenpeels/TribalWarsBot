import copy
import logging

from src.core.config import Config
from src.core.file_manager import FileManager
from src.core.input import Input
from src.core.page_parser import PageParser
from src.core.time_utils import TimeUtils
from src.core.web_wrapper import WebWrapper
from src.game.village import Village

logger = logging.getLogger("Bot")


class Bot:
    villages: [Village] = []

    def __init__(self, config: Config):
        self.config = config
        self.web = WebWrapper(self.config)

        self.setup_environment()

    def start(self):
        logger.info("Bot started")

        self.villages = self.get_villages()

        while True:
            for village in self.villages:
                village.run()
                sleep_time_village = self.config.get("bot.delays.between_villages", 5)
                logger.info(f"Sleeping for {sleep_time_village} seconds")
                TimeUtils.sleep(sleep_time_village)

            sleep_time_runs = self.config.get("bot.delays.between_runs", 180)
            logger.info(f"Sleeping for {sleep_time_runs} seconds")
            TimeUtils.sleep(sleep_time_runs)

    def get_villages(self):
        logger.info("Getting villages")
        result = self.web.get_screen("overview_villages")
        villages = PageParser.get_villages_from_overview(result)

        # Remove villages that are already in the config
        config_villages = self.config.get("villages", [])
        new_villages = []
        for village_id, village_name in villages:
            existing_village = next((village for village in config_villages if village["id"] == village_id), None)
            if not existing_village:
                new_villages.append((village_id, village_name))

        # Should we manage new villages?
        auto_manage = self.config.get("bot.auto_manage_new_villages", False)
        for village_id, village_name in new_villages:
            should_manage = auto_manage or Input.ask_bool(f"Manage village \"{village_name}\"?")
            new_village = copy.deepcopy(self.config.get("village_template"))
            new_village.update({
                "id": village_id,
                "name": village_name,
                "manage": should_manage
            })
            config_villages.append(new_village)

        # Save the new villages to the config
        self.config.set("villages", config_villages)

        # Create Village objects
        return [Village(village_config, self.config, self.web) for village_config in config_villages]

    @staticmethod
    def setup_environment():
        FileManager.create_directory("data")
