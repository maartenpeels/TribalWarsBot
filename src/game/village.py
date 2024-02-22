import logging
import math

from src.core.config import Config
from src.core.events import publish_event, Event
from src.core.page_parser import PageParser
from src.core.web_wrapper import WebWrapper
from src.game.managers.building_manager import BuildingManager

logger = logging.getLogger("Village")


class Village:
    def __init__(self, village_config, config: Config, web: WebWrapper):
        self.config = config
        self.village_config = village_config
        self.village_id = village_config["id"]
        self.village_name = village_config["name"]
        self.web = web

        global logger
        logger = logging.getLogger(f"Village \"{self.village_config['name']}\"")

        self.building_manager = BuildingManager(self.village_id, self.village_name, self.config, self.web)

        self.village_data = self.get_data()
        self.log_info()

    def run(self):
        logger.info("Starting run")
        self.get_data()
        self.building_manager.run()

    def log_info(self):
        wood_prod_hour = math.floor(self.village_data.wood_prod * 60 * 60)
        stone_prod_hour = math.floor(self.village_data.stone_prod * 60 * 60)
        iron_prod_hour = math.floor(self.village_data.iron_prod * 60 * 60)

        logger.info(
            f"Wood: {self.village_data.wood}({wood_prod_hour}/h), "
            f"Stone: {self.village_data.stone}({stone_prod_hour}/h), "
            f"Iron: {self.village_data.iron}({iron_prod_hour}/h)")
        logger.info(f"Population: {self.village_data.pop}/{self.village_data.pop_max}")
        logger.info(f"Max storage: {self.village_data.storage_max}")

    def get_data(self):
        logger.debug("Getting village data")
        result = self.web.get_screen("overview_village", params={"village": self.village_id})
        village_data = PageParser.get_village_data_from_village_overview(result)
        publish_event(Event.VILLAGE_DATA_UPDATE, village_data)
        return village_data
