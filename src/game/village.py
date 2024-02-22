import logging

logger = logging.getLogger("Village")


class Village:
    def __init__(self, village_config, web):
        self.village_config = village_config
        self.web = web

        global logger
        logger = logging.getLogger(f"Village \"{self.village_config['name']}\"")

        self.get_data()

    def get_data(self):
        logger.info("Getting village data")
        # result = self.web.get_screen("overview_village", params={"village": self.village_id})
        # return PageParser.get_village_data(result)
        pass
