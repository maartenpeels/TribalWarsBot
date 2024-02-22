import logging
import math

from src.core.page_parser import PageParser

logger = logging.getLogger("Village")


class Village:
    def __init__(self, village_config, web):
        self.village_config = village_config
        self.village_id = village_config["id"]
        self.village_name = village_config["name"]
        self.web = web

        global logger
        logger = logging.getLogger(f"Village \"{self.village_config['name']}\"")

        self.village_data = self.get_data()
        self.log_info()

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
        logger.info("Getting village data")
        result = self.web.get_screen("overview_village", params={"village": self.village_id})
        return PageParser.get_village_data(result)
